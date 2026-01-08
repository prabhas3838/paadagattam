from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


from database import SessionLocal
from schemas import CandidateCreate, PreferenceCreate
from crud import (
    create_candidate,
    get_candidate,
    add_preference,
    submit_candidate
)
from allocation import (
    run_allocation,
    withdraw_seat,
    opt_for_sliding,
    hold_seat
)
from rounds import (
    is_round_open,
    get_round_status,
    get_active_round
)
app = FastAPI(title="Voice-Based Admission Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from models import SeatMatrix, Allocation




# -------------------------------------------------
# Database Dependency
# -------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------
# OPTIONS (Courses + Campuses)
# -------------------------------------------------
@app.get("/options")
def get_options(db: Session = Depends(get_db)):
    seats = db.query(SeatMatrix).all()
    return [
        {
            "course": s.course,
            "campus": s.campus,
            "remaining_seats": s.remaining_seats
        }
        for s in seats
    ]


# -------------------------------------------------
# CANDIDATE REGISTRATION
# -------------------------------------------------
@app.post("/candidate")
def register_candidate(
    data: CandidateCreate,
    db: Session = Depends(get_db)
):
    return create_candidate(db, data.candidate_id, data.aeee_rank)


# -------------------------------------------------
# ADD / UPDATE PREFERENCE
# -------------------------------------------------
@app.post("/candidate/{candidate_id}/preference")
def add_pref(
    candidate_id: str,
    pref: PreferenceCreate,
    db: Session = Depends(get_db)
):
    current_round = get_active_round(db)

    if not current_round:
        return {"error": "No active admission round"}

    if not is_round_open(db, current_round):
        return {
            "error": f"Preference window is closed for Round {current_round}"
        }

    candidate = get_candidate(db, candidate_id)
    if not candidate:
        return {"error": "Candidate not found"}

    add_preference(db, candidate, pref)

    return {
        "message": f"Preference added for Round {current_round}"
    }


# -------------------------------------------------
# VIEW PREFERENCES
# -------------------------------------------------
@app.get("/candidate/{candidate_id}/preferences")
def view_preferences(candidate_id: str, db: Session = Depends(get_db)):
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        return {"error": "Candidate not found"}

    return candidate.preferences


# -------------------------------------------------
# SUBMIT PREFERENCES
# -------------------------------------------------
@app.post("/candidate/{candidate_id}/submit")
def submit(candidate_id: str, db: Session = Depends(get_db)):
    current_round = get_active_round(db)

    if not current_round:
        return {"error": "No active admission round"}

    if not is_round_open(db, current_round):
        return {"error": "Preference window is closed"}

    candidate = get_candidate(db, candidate_id)
    if not candidate:
        return {"error": "Candidate not found"}

    submit_candidate(db, candidate)

    return {
        "message": f"Preferences submitted for Round {current_round}"
    }


# -------------------------------------------------
# ROUND STATUS (TIMER)
# -------------------------------------------------
@app.get("/round/{round_no}/status")
def round_status(round_no: int, db: Session = Depends(get_db)):
    return get_round_status(db, round_no)


# -------------------------------------------------
# RUN ALLOCATION (ROUND-WISE)
# -------------------------------------------------
@app.post("/allocate/round/{round_no}")
def allocate_round(round_no: int, db: Session = Depends(get_db)):
    status = get_round_status(db, round_no)

    if status["status"] != "CLOSED":
        return {
            "error": f"Allocation can run only after Round {round_no} closes"
        }

    run_allocation(db, round_no)
    return {
        "message": f"Round {round_no} allocation completed"
    }


# -------------------------------------------------
# VIEW ALL ALLOCATIONS
# -------------------------------------------------
@app.get("/allocations")
def view_allocations(db: Session = Depends(get_db)):
    return db.query(Allocation).all()


# -------------------------------------------------
# USER ACTIONS AFTER ALLOCATION
# -------------------------------------------------

@app.post("/candidate/{candidate_id}/withdraw")
def withdraw(candidate_id: str, db: Session = Depends(get_db)):
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        return {"error": "Candidate not found"}

    success = withdraw_seat(db, candidate.id)
    if not success:
        return {"error": "No active seat to withdraw"}

    return {
        "message": "Seat withdrawn successfully. Seat released for next round."
    }


@app.post("/candidate/{candidate_id}/slide")
def slide(candidate_id: str, db: Session = Depends(get_db)):
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        return {"error": "Candidate not found"}

    success = opt_for_sliding(db, candidate.id)
    if not success:
        return {"error": "No held seat available for sliding"}

    return {
        "message": "You have opted for sliding in the next round"
    }


@app.post("/candidate/{candidate_id}/hold")
def hold(candidate_id: str, db: Session = Depends(get_db)):
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        return {"error": "Candidate not found"}

    success = hold_seat(db, candidate.id)
    if not success:
        return {"error": "No seat found to hold"}

    return {
        "message": "Seat confirmed and locked"
    }
@app.get("/candidate/{candidate_id}/allocation")
def get_my_allocation(candidate_id: str, db: Session = Depends(get_db)):
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        return None

    allocation = (
        db.query(Allocation)
        .filter(Allocation.candidate_id == candidate.id)
        .order_by(Allocation.round.desc())
        .first()
    )

    return allocation


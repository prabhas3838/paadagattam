# allocation.py

from sqlalchemy.orm import Session
from models import Candidate, SeatMatrix, Allocation,Preference


# -------------------------------------------------
# Helper functions
# -------------------------------------------------

def get_current_allocation(db: Session, candidate_id: int):
    """
    Returns the latest allocation for a candidate (if any).
    """
    return (
        db.query(Allocation)
        .filter(Allocation.candidate_id == candidate_id)
        .order_by(Allocation.round.desc())
        .first()
    )


def release_seat(db: Session, allocation: Allocation):
    """
    Releases a seat back to seat_matrix.
    """
    seat = (
        db.query(SeatMatrix)
        .filter(
            SeatMatrix.course == allocation.course,
            SeatMatrix.campus == allocation.campus
        )
        .with_for_update()
        .first()
    )

    if seat:
        seat.remaining_seats += 1


# -------------------------------------------------
# USER ACTIONS (CRITICAL)
# -------------------------------------------------
def withdraw_seat(db: Session, candidate_id: int) -> bool:
    """
    Candidate withdraws permanently.
    Seat is released and candidate is removed from system.
    """

    # 1️⃣ Find HELD allocation
    allocation = (
        db.query(Allocation)
        .filter(
            Allocation.candidate_id == candidate_id,
            Allocation.seat_status == "HELD"
        )
        .order_by(Allocation.round.desc())
        .with_for_update()
        .first()
    )

    if not allocation:
        return False

    # 2️⃣ Release seat
    release_seat(db, allocation)

    # 3️⃣ Delete allocation records
    db.query(Allocation).filter(
        Allocation.candidate_id == candidate_id
    ).delete()

    # 4️⃣ Delete preferences
    db.query(Preference).filter(
        Preference.candidate_id == candidate_id
    ).delete()

    # 5️⃣ Delete candidate
    db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).delete()

    db.commit()
    return True




def opt_for_sliding(db: Session, candidate_id: int):
    """
    Candidate opts for sliding in next round.
    """
    allocation = get_current_allocation(db, candidate_id)

    if not allocation or allocation.seat_status != "HELD":
        return False

    allocation.seat_status = "SLIDING"
    db.commit()
    return True


def hold_seat(db: Session, candidate_id: int):
    """
    Candidate confirms and locks seat.
    """
    allocation = get_current_allocation(db, candidate_id)

    if not allocation:
        return False

    allocation.seat_status = "HELD"
    db.commit()
    return True


# -------------------------------------------------
# ROUND 1 ALLOCATION
# -------------------------------------------------

def run_round1_allocation(db: Session):
    """
    Round 1:
    - Only candidates with NO allocation
    - Allocate based on rank & preference order
    """

    candidates = (
        db.query(Candidate)
        .filter(Candidate.submitted == True)
        .order_by(Candidate.aeee_rank)
        .all()
    )

    for candidate in candidates:
        if get_current_allocation(db, candidate.id):
            continue

        preferences = sorted(candidate.preferences, key=lambda p: p.priority)

        for pref in preferences:
            seat = (
                db.query(SeatMatrix)
                .filter(
                    SeatMatrix.course == pref.course,
                    SeatMatrix.campus == pref.campus
                )
                .with_for_update()
                .first()
            )

            if seat and seat.remaining_seats > 0:
                seat.remaining_seats -= 1

                db.add(
                    Allocation(
                        candidate_id=candidate.id,
                        course=pref.course,
                        campus=pref.campus,
                        round=1,
                        seat_status="HELD"
                    )
                )
                break

    db.commit()


# -------------------------------------------------
# ROUND 2 SLIDING / UPGRADE LOGIC
# -------------------------------------------------

def run_round2_sliding(db: Session):
    """
    Round 2:
    - Candidates with no seat OR seat_status = SLIDING
    - Try to upgrade to higher preferences only
    - Never lose existing seat
    """

    candidates = (
        db.query(Candidate)
        .filter(Candidate.submitted == True)
        .order_by(Candidate.aeee_rank)
        .all()
    )

    for candidate in candidates:
        current_alloc = get_current_allocation(db, candidate.id)

        # Case 1: Candidate has no seat
        if not current_alloc:
            preferences = sorted(candidate.preferences, key=lambda p: p.priority)

            for pref in preferences:
                seat = (
                    db.query(SeatMatrix)
                    .filter(
                        SeatMatrix.course == pref.course,
                        SeatMatrix.campus == pref.campus
                    )
                    .with_for_update()
                    .first()
                )

                if seat and seat.remaining_seats > 0:
                    seat.remaining_seats -= 1

                    db.add(
                        Allocation(
                            candidate_id=candidate.id,
                            course=pref.course,
                            campus=pref.campus,
                            round=2,
                            seat_status="HELD"
                        )
                    )
                    break

        # Case 2: Candidate opted for sliding
        elif current_alloc.seat_status == "SLIDING":
            preferences = sorted(candidate.preferences, key=lambda p: p.priority)

            current_index = None
            for i, pref in enumerate(preferences):
                if pref.course == current_alloc.course and pref.campus == current_alloc.campus:
                    current_index = i
                    break

            if current_index is not None:
                higher_prefs = preferences[:current_index]

                for pref in higher_prefs:
                    seat = (
                        db.query(SeatMatrix)
                        .filter(
                            SeatMatrix.course == pref.course,
                            SeatMatrix.campus == pref.campus
                        )
                        .with_for_update()
                        .first()
                    )

                    if seat and seat.remaining_seats > 0:
                        release_seat(db, current_alloc)
                        seat.remaining_seats -= 1

                        db.add(
                            Allocation(
                                candidate_id=candidate.id,
                                course=pref.course,
                                campus=pref.campus,
                                round=2,
                                seat_status="HELD"
                            )
                        )
                        break

    db.commit()


# -------------------------------------------------
# ENTRY POINT
# -------------------------------------------------

def run_allocation(db: Session, round_no: int):
    """
    Dispatch allocation logic based on round number.
    """
    if round_no == 1:
        run_round1_allocation(db)
    elif round_no == 2:
        run_round2_sliding(db)
    else:
        raise ValueError("Unsupported round number")

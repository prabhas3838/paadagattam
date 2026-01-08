from sqlalchemy.orm import Session
from models import Candidate, Preference

def create_candidate(db: Session, candidate_id: str, rank: int):
    candidate = Candidate(candidate_id=candidate_id, aeee_rank=rank)
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate


def get_candidate(db: Session, candidate_id: str):
    return db.query(Candidate).filter_by(candidate_id=candidate_id).first()


def add_preference(db: Session, candidate: Candidate, pref):
    db.query(Preference).filter(
        Preference.candidate_id == candidate.id,
        Preference.priority == pref.priority
    ).delete()

    preference = Preference(
        course=pref.course,
        campus=pref.campus,
        priority=pref.priority,
        candidate=candidate
    )
    db.add(preference)
    db.commit()


def submit_candidate(db: Session, candidate: Candidate):
    candidate.submitted = True
    db.commit()

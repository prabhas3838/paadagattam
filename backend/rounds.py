# rounds.py

from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models import AdmissionRound


def is_round_open(db: Session, round_no: int) -> bool:
    """
    Returns True if the preference window for the given round is OPEN.
    """
    now = datetime.now()


    return (
        db.query(AdmissionRound)
        .filter(
            AdmissionRound.round_number == round_no,
            AdmissionRound.start_time <= now,
            AdmissionRound.end_time >= now,
            AdmissionRound.active == True
        )
        .first()
        is not None
    )


def get_round_status(db: Session, round_no: int):
    """
    Returns round status and remaining time.
    Used by frontend to show countdown.
    """
    now = datetime.now()


    round_obj = (
        db.query(AdmissionRound)
        .filter(AdmissionRound.round_number == round_no)
        .first()
    )

    if not round_obj:
        return {
            "round": round_no,
            "status": "NOT_CONFIGURED",
            "seconds_remaining": None
        }

    if now < round_obj.start_time:
        return {
            "round": round_no,
            "status": "NOT_STARTED",
            "seconds_remaining": int(
                (round_obj.start_time - now).total_seconds()
            )
        }

    if now > round_obj.end_time:
        return {
            "round": round_no,
            "status": "CLOSED",
            "seconds_remaining": 0
        }

    return {
        "round": round_no,
        "status": "OPEN",
        "seconds_remaining": int(
            (round_obj.end_time - now).total_seconds()
        )
    }


def get_active_round(db: Session):
    """
    Returns the currently active round number.
    If multiple rounds overlap, returns the lowest round number.
    """
    now = datetime.now()


    round_obj = (
        db.query(AdmissionRound)
        .filter(
            AdmissionRound.start_time <= now,
            AdmissionRound.end_time >= now,
            AdmissionRound.active == True
        )
        .order_by(AdmissionRound.round_number.asc())
        .first()
    )

    return round_obj.round_number if round_obj else None

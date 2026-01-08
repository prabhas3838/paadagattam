from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True)
    candidate_id = Column(String, unique=True, index=True)
    aeee_rank = Column(Integer)
    submitted = Column(Boolean, default=False)

    preferences = relationship("Preference", back_populates="candidate")


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True)
    course = Column(String)
    campus = Column(String)
    priority = Column(Integer)

    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    candidate = relationship("Candidate", back_populates="preferences")


class SeatMatrix(Base):
    __tablename__ = "seat_matrix"

    id = Column(Integer, primary_key=True)
    course = Column(String)
    campus = Column(String)
    total_seats = Column(Integer)
    remaining_seats = Column(Integer)


from sqlalchemy import Column, Integer, String
from database import Base

class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer)
    course = Column(String)
    campus = Column(String)
    round = Column(Integer)
    seat_status = Column(String, default="HELD")  
    # HELD | SLIDING | WITHDRAWN




# models.py

from sqlalchemy import Column, Integer, Boolean, DateTime
from database import Base

class AdmissionRound(Base):
    __tablename__ = "admission_rounds"

    id = Column(Integer, primary_key=True)
    round_number = Column(Integer, unique=True, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    active = Column(Boolean, default=True)


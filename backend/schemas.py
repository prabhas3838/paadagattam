from pydantic import BaseModel
from typing import List

class CandidateCreate(BaseModel):
    candidate_id: str
    aeee_rank: int


class PreferenceCreate(BaseModel):
    course: str
    campus: str
    priority: int

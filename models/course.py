from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Course(BaseModel):
    course_id: Optional[int]=0
    name: str
    date: datetime
    description: str
    domain: List[str]
    chapters: List[dict]
    rating: Optional[float]=0


def info():
    return "hello"
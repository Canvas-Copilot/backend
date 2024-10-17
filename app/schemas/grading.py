from typing import Dict, List, Optional
from pydantic import BaseModel

from app.schemas.canvas import (
    Assignment,
    Course,
    FeedbackSettings,
    GradingSettings,
    Submission,
)


# Define RequestGradingDto
class RequestGradingDto(BaseModel):
    course: Course
    assignment: Assignment
    submissions: List[Submission]
    grading_settings: Optional[GradingSettings] = None
    feedback_settings: Optional[FeedbackSettings] = None


class GradingFeedback(BaseModel):
    submission_id: int
    score: float
    feedback: str


GradingFeedbackResponse = Dict[int, GradingFeedback]

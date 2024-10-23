from enum import Enum
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime


class CanvasSettings(BaseModel):
    """
    Schema for Canvas API settings.
    """

    canvas_url: HttpUrl = Field(..., example="https://canvas.example.com")
    canvas_api_token: str = Field(..., min_length=10, example="your_canvas_api_token")


class GradingType(str, Enum):
    pass_fail = "pass_fail"
    percent = "percent"
    letter_grade = "letter_grade"
    gpa_scale = "gpa_scale"
    points = "points"


class SubmissionType(str, Enum):
    online_text_entry = "online_text_entry"
    online_url = "online_url"
    online_upload = "online_upload"
    online_quiz = "online_quiz"
    media_recording = "media_recording"


class WorkflowState(str, Enum):
    submitted = "submitted"
    unsubmitted = "unsubmitted"
    graded = "graded"
    pending_review = "pending_review"


class Assignment(BaseModel):
    """
    Schema representing an assignment fetched from Canvas.
    """

    id: int
    name: str
    description: str
    course_id: int
    created_at: str
    updated_at: str
    due_at: Optional[str] = None
    html_url: str
    points_possible: float
    grading_type: GradingType
    submissions_download_url: str
    assignment_group_id: int
    submission_types: List[SubmissionType]
    has_submitted_submissions: bool
    needs_grading_count: Optional[int] = None

    class Config:
        from_attributes = True


class Submission(BaseModel):
    """
    Schema representing a submission fetched from Canvas.
    """

    id: int
    body: Optional[str] = None
    url: Optional[str] = None
    assignment_id: int
    user_id: int
    submission_type: Optional[SubmissionType]
    workflow_state: WorkflowState
    grade_matches_current_submission: bool
    late: bool
    missing: bool
    preview_url: str
    attachments: Optional[List["Attachment"]] = None

    class Config:
        from_attributes = True


class Attachment(BaseModel):
    id: int
    uuid: str
    folder_id: str | int
    display_name: str
    filename: str
    upload_status: str
    content_type: str = Field(..., alias="content-type")
    url: str
    size: int
    created_at: datetime
    updated_at: datetime
    modified_at: datetime
    mime_class: str
    preview_url: str

    class Config:
        populate_by_name = True


class EnrollmentType(str, Enum):
    teacher = "teacher"
    student = "student"
    ta = "ta"
    observer = "observer"
    designer = "designer"


class EnrollmentState(str, Enum):
    active = "active"
    invited_or_pending = "invited_or_pending"
    completed = "completed"


class Enrollment(BaseModel):
    type: EnrollmentType
    user_id: int
    enrollment_state: EnrollmentState


class Course(BaseModel):
    id: int
    name: str
    account_id: int
    end_at: Optional[str] = None
    uuid: str
    course_code: str
    created_at: str
    enrollments: List[Enrollment]
    needs_grading_count: Optional[int] = None


class User(BaseModel):
    id: int
    name: str
    created_at: str
    sortable_name: str
    short_name: str
    avatar_url: str
    last_name: str
    first_name: str


class CanvasAPIResponse(BaseModel):
    """
    Generic schema for Canvas API responses.
    """

    data: List[dict]

    class Config:
        from_attributes = True


class StrictnessLevel(str, Enum):
    strict = "strict"
    moderate = "moderate"
    loose = "loose"


class FeedbackTone(str, Enum):
    formal = "formal"
    friendly = "friendly"
    constructive = "constructive"


class FeedbackLength(str, Enum):
    short = "short"
    medium = "medium"
    detailed = "detailed"


# Define GradingSettings and FeedbackSettings
class GradingSettings(BaseModel):
    strictness: Optional[StrictnessLevel] = StrictnessLevel.moderate


class FeedbackSettings(BaseModel):
    tone: Optional[FeedbackTone] = FeedbackTone.constructive
    length: Optional[FeedbackLength] = FeedbackLength.medium
    custom_feedback_prompt: Optional[str] = None

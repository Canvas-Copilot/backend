from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, Request
from bs4 import BeautifulSoup
import json
import re
import requests

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

    class Config:
        from_attributes = True


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
    enabled: bool
    strictness: Optional[StrictnessLevel] = StrictnessLevel.moderate


class FeedbackSettings(BaseModel):
    enabled: bool
    tone: Optional[FeedbackTone] = FeedbackTone.constructive
    length: Optional[FeedbackLength] = FeedbackLength.medium
    custom_feedback_prompt: Optional[str] = None


# input data
class RequestGradingDto(BaseModel):
    course: Course
    assignment: Assignment
    submissions: List[Submission]
    grading_settings: Optional[GradingSettings] = None
    feedback_settings: Optional[FeedbackSettings] = None


class GradingFeedback(BaseModel):
    submission_id: int
    grade: float
    feedback: str


# output data:
# submission_id -> GradingFeedback
GradingFeedbackResponse = Dict[int, GradingFeedback]


app = FastAPI()


class OllamaRequest(BaseModel):
    model: str
    input: str


def call_ollama_api(prompt: str) -> str:
    url = 'http://localhost:11434/api/generate'
    headers = {'Content-Type': 'application/json'}
    data = {
        "model": "llama3",
        "prompt": prompt
    }

    # 打开流式请求，逐步获取数据
    with requests.post(url, json=data, headers=headers, stream=True) as response:
        if response.status_code == 200:
            result = ""
            # 逐行读取响应数据
            for line in response.iter_lines():
                if line:
                    # 尝试解析每一行 JSON 数据
                    try:
                        line_data = line.decode('utf-8')
                        json_line = json.loads(line_data)
                        # 累积生成的响应文本
                        result += json_line.get('response', '')
                    except ValueError as e:
                        raise Exception(f"Error parsing JSON line: {line_data}")

            return result or "No feedback generated"
        else:
            raise Exception(f"Error calling Ollama API: {response.status_code}")


@app.post("/generate", response_model=dict)
async def generate_grading_feedback(request: Request) -> GradingFeedbackResponse:
    # Parse incoming data
    grading_data = await request.json()
    dto = RequestGradingDto(**grading_data)

    feedback_response = {}

    for submission in dto.submissions:
        # Create prompt for each submission
        prompt = (f"<Assignment> <name>'{dto.assignment.name}'</name><content>{BeautifulSoup(submission.body, 'html.parser').get_text()}</content></Assignment> "
                  f"Give a feedback and a clear score for this assignment,"
                  f"based on this criteria: {BeautifulSoup(dto.assignment.description, 'html.parser').get_text()}."
                  f"You should respond using XML tag like this:'<FEEDBACK>your feedback here<FEEDBACK><SCORE>your score (use format like 'score'/{(dto.assignment.points_possible):.2f}(which is the full score here)) here</SCORE>' "
                  )

        # Call Ollama API for feedback
        feedback = call_ollama_api(prompt)
        match = re.search(r"<SCORE>(\d+\.\d+|\d+)/(\d+\.\d+|\d+)</SCORE>", feedback)

        # Calculate grade
        match_grade = float(match.group(1))

        # Store feedback and grade for this submission
        feedback_response[submission.id] = GradingFeedback(
            submission_id=submission.id,
            grade=match_grade, #match_grade,
            feedback=feedback
        )

    # Return a dictionary of feedbacks for all submissions
    return feedback_response

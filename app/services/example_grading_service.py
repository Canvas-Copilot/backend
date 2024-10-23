from app.schemas.grading import (
    GradingArgs,
    GradingFeedbackResponse,
)

def generate_grading_feedback(grading_args: GradingArgs) -> GradingFeedbackResponse: ...

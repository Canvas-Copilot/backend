from app.celery_app import celery_app
from app.schemas.grading import RequestGradingDto
from app.services.project_service import generate_grading_feedback
from fastapi.encoders import jsonable_encoder


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def generate_grading_feedback_task(self, user_id: int, request_data: dict):
    # Deserialize request_data into Pydantic model
    request = RequestGradingDto(**request_data)
    response = generate_grading_feedback(request)

    json_response = jsonable_encoder(response)

    return json_response

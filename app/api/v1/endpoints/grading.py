from celery.result import AsyncResult
from app.celery_app import celery_app
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_auth
from app.schemas.grading import RequestGradingDto
from app.utils.logger import logger
from app.tasks.grading_tasks import generate_grading_feedback_task

router = APIRouter()


@router.post("/generate", response_model=dict)
def generate_grading_feedback(
    request: RequestGradingDto, auth: str = Depends(get_auth)
):
    """
    Enqueue a grading and feedback generation task.
    Returns a task_id to track the task status and retrieve results.
    """
    print("Request: ", request.model_dump_json())
    try:
        # Serialize the RequestGradingDto to a dictionary
        request_data = request.model_dump()

        # Enqueue the Celery task
        task = generate_grading_feedback_task.apply_async(args=(auth, request_data))
        return {"task_id": task.id}

    except Exception as e:
        logger.error(f"Error enqueuing grading task: {e}")
        raise HTTPException(status_code=500, detail="Failed to enqueue grading task.")


@router.get("/status/{task_id}", response_model=dict)
def get_task_status(task_id: str):
    """
    Retrieve the status of a Celery task.
    """
    try:
        task_result = AsyncResult(task_id, app=celery_app)
        response = {
            "task_id": task_id,
            "status": task_result.status,
            "result": task_result.result if task_result.status == "SUCCESS" else None,
            "traceback": (
                "Failed to generate feedback."
                if task_result.status == "FAILURE"
                else None
            ),
        }
        return response
    except Exception as e:
        logger.error(f"Error retrieving task status for {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve task status.")

from pydantic import BaseModel
import json
import requests
from app.schemas.grading import (
    GradingFeedback,
    GradingFeedbackResponse,
    RequestGradingDto,
)


class OllamaRequest(BaseModel):
    model: str
    input: str


def call_ollama_api(prompt: str) -> str:
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {"model": "llama3.2", "prompt": prompt}

    # 打开流式请求，逐步获取数据
    with requests.post(url, json=data, headers=headers, stream=True) as response:
        if response.status_code == 200:
            result = ""
            # 逐行读取响应数据
            for line in response.iter_lines():
                if line:
                    # 尝试解析每一行 JSON 数据
                    try:
                        line_data = line.decode("utf-8")
                        json_line = json.loads(line_data)
                        # 累积生成的响应文本
                        result += json_line.get("response", "")
                    except ValueError as e:
                        raise Exception(f"Error parsing JSON line: {line_data}")

            return result or "No feedback generated"
        else:
            raise Exception(f"Error calling Ollama API: {response.status_code}")


def generate_grading_feedback(dto: RequestGradingDto) -> GradingFeedbackResponse:
    # Parse incoming data
    feedback_response = {}

    for submission in dto.submissions:
        # Create prompt for each submission
        prompt = f"Grading assignment '{dto.assignment.name}' for course {dto.course.name}. Submission content: {submission.body}"

        # Call Ollama API for feedback
        feedback = call_ollama_api(prompt)

        # Calculate grade dynamically based on points_possible
        # Here we assume a default grade percentage of 85%
        grade_percentage = 0.85
        grade = dto.assignment.points_possible * grade_percentage

        # Store feedback and grade for this submission
        feedback_response[submission.id] = GradingFeedback(
            submission_id=submission.id, score=grade, feedback=feedback
        )

    # Return a dictionary of feedbacks for all submissions
    return feedback_response

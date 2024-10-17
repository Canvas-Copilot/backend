from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.v1.endpoints import grading
from app.middleware import DuplicateBodyMiddleware
from app.utils.logger import logger
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Canvas Copilot Backend",
    description="Backend server for Canvas Copilot - a tool to assist in grading Canvas assignments",
    version="1.0.0",
)

# Include Routers
app.include_router(grading.router, prefix="/api/v1/grading", tags=["grading"])

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(DuplicateBodyMiddleware)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    # Log the validation error and request body
    logger.error(f"Validation error: {exc}")
    # Return the default 422 response
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

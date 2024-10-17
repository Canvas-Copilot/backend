from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


# Middleware to read and store the request body
class DuplicateBodyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Read the body
        body = await request.body()
        # Store the body in request.state
        request.state.body = body

        # Replace the receive method so downstream can read the body
        async def receive():
            return {"type": "http.request", "body": body}

        request._receive = receive
        # Proceed with the request
        response = await call_next(request)
        return response

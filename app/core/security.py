from fastapi import Header, HTTPException, status


def get_auth(x_auth: str = Header(None)) -> str:
    # if not x_canvas_auth:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

    return x_auth or "test"

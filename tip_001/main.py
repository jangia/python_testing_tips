from fastapi import FastAPI, HTTPException
from starlette import status

USERS = [
    {"user_id": 1, "name": "John Doe"},
    {"user_id": 2, "name": "Jane Doe"},
]

app = FastAPI()


@app.get("/user/{user_id}")
def user_details(user_id: int):
    user = next((user for user in USERS if user["user_id"] == user_id), None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user

from fastapi import FastAPI, HTTPException, Path
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    age: int

users = []

@app.get("/users")
async def get_users():
    return users

@app.post("/user/{username}/{age}")
async def create_user(username: Annotated[str, Path(min_length=3, max_length=20, regex="^[a-zA-Z0-9_-]+$")],
                      age: Annotated[int, Path(ge=18, le=100, description="Age from 18 to 100")]):
    if users:
        new_id = users[-1].id + 1
    else:
        new_id = 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='75')],
                      username: Annotated[str, Path(min_length=3, max_length=20, regex="^[a-zA-Z0-9_-]+$")],
                      age: Annotated[int, Path(ge=18, le=100, description="Age from 18 to 100")]):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User  was not found")

@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='75')]):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User  was not found")


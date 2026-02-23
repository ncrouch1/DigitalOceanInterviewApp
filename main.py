from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from db import DatabaseWrapper
import psycopg2
import os

import uuid

load_dotenv()
app = FastAPI()
database_url = os.getenv("DATABASE_URL")

databaseWrapper = DatabaseWrapper(database_url)

class CreateUserRequest(BaseModel):
    username: str

class UpdateScoreRequest(BaseModel):
    userId: uuid.UUID
    score: int

class GetScoreRequest(BaseModel):
    userId: uuid.UUID

class GetTopXScoresRequest(BaseModel):
    x: int

@app.post("/updateScore")
async def updateScore(request: UpdateScoreRequest): 
    databaseWrapper.update_score(request.userId, request.score)
    return {"message": "Score updated successfully"}

@app.get("/getScore")
async def getScore(request: GetScoreRequest):
    data = databaseWrapper.get_score(request.userId)
    if data is not None:
        return {"score": data}
    else:
        return {"message": "User not found"}, 404

@app.get("/getTopXScores")
async def getTopXScores(request: GetTopXScoresRequest): 
    data = databaseWrapper.get_top_x_scores(request.x)
    return {"top_scores": data}

@app.post("/createUser")
async def createUser(request: CreateUserRequest):
    user_id = databaseWrapper.create_user(request.username)
    return {"userId": user_id}
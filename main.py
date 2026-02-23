from fastapi import FastApi
from pydantic import BaseModel
import psycopg2

import uuid

app = FastApi()
database_url = env.get("DATABASE_URL")


databaseWrapper = DatabaseWrapper(database_url)


class User(BaseModel):
    id: uuid.SafeUUID
    username: str
    score: int


@app.post("/updateScore")
async def updateScore(userId: uuid.SafeUUID, score: int): 
    pass

@app.get("/getScore")
async def getScore(userId: uuid.SafeUUID):
    pass

@app.get("/getTopXScores")
async def getTop100Scores(): 
    pass

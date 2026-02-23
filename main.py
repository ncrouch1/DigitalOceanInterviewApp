from fastapi import FastApi
from pydantic import BaseModel
import psycopg2

import uuid

app = FastApi()
conn = None

try:
    conn = psycopg2.connect(
        database="your_database_name",
        user="your_username",
        password="your_password",
        host="your_host_address",
        port="5432"
    )
    print("Connection successful")
except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL: {e}")
    conn = None



class User(BaseModel):
    id: uuid.SafeUUID
    username: str
    score: int


@app.post("/updateScore")
async def updateScore(userId: uuid.SafeUUID, score: int): 
    pass

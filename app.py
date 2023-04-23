from fastapi import FastAPI, Query
from transformers import pipeline
from pydantic import BaseModel, Field
from typing import Dict

sentiment_analysis_model_name = 'distilbert-base-uncased-finetuned-sst-2-english'

app = FastAPI()

class InputData(BaseModel):
    phrase: str = Field(...,
        min_length=1, max_length=300,
        description="Phrase to apply against an ML model to gather a sentiment analysis.")

class OutputData(BaseModel):
    result: Dict

@app.get("/")
async def hello_world(name: str = Query(..., min_length=1, max_length=50, description="Your name")):
    return {"message": f"Hello, {name}!"}

@app.post("/ml", response_model=OutputData)
async def ml(
    input_data: InputData
) -> OutputData:
    output = pipeline(sentiment_analysis_model_name)(input_data)
    return output

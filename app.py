from fastapi import FastAPI, Query
from transformers import pipeline
from pydantic import BaseModel, Field

model_name = 'distilbert-base-uncased-finetuned-sst-2-english'

app = FastAPI()

class InputData(BaseModel):
    input_data: str = Field(..., min_length=1, description="Input data must be at least 1 character long")

@app.get("/")
async def hello_world(name: str = Query(..., min_length=1, max_length=50, description="Your name")):
    return {"message": f"Hello, {name}!"}

@app.post("/ml")
async def ml(json: InputData):
    output = pipeline(task = 'sentiment-analysis',
                      model = model_name)(json.input_data)[0]
    output['input_data'] = json.input_data
    return output

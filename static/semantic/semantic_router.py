from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from transformers import pipeline
from pydantic import BaseModel, Field

model_name = 'distilbert-base-uncased-finetuned-sst-2-english'

class InputData(BaseModel):
    input_data: str = Field(..., min_length=1, description="Input data must be at least 1 character long")

router = APIRouter()

@router.post("/")
async def semantic(json: InputData):
    output = pipeline(task = 'sentiment-analysis',
                      model = model_name)(json.input_data)[0]
    output['input_data'] = json.input_data
    return output

from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from transformers import pipeline
from pydantic import BaseModel, Field
import pdb

'''
Sentiment Router
This file is basically my "controller" (MVC) for handling requests
related to this area of study.
'''

router = APIRouter()

model_name = 'distilbert-base-uncased-finetuned-sst-2-english'

class InputData(BaseModel):
    input_data: str = Field(..., min_length=1, description="Input data must be at least 1 character long")


templates = Jinja2Templates(directory="templates")

@router.get("")
async def sentiment(request: Request):
    # pdb.set_trace() # for debugging
    return templates.TemplateResponse("sentiment.html", {
        "request": request })

@router.post("")
async def sentiment(json: InputData):
    output = pipeline(task = 'sentiment-analysis',
                      model = model_name)(json.input_data)[0]
    output['input_data'] = json.input_data
    return output

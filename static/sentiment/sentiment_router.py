from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from transformers import pipeline
from pydantic import BaseModel, Field

from helpers.jinja_helpers import build_templates_and_router

# Sentiment Router
# Here we're using HuggingFace's Transformers library to load up a small
# and simple Language model that's able to do crude sentiment analysis on
# snippets of text that we pass to it.

templates, router, module_name = build_templates_and_router(__file__)
model_name = 'distilbert-base-uncased-finetuned-sst-2-english'

class InputData(BaseModel):
    input_data: str = Field(..., min_length=1, description="Input data must be at least 1 character long")

@router.get("")
async def sentiment(request: Request):
    return templates.TemplateResponse("static/" + module_name + "/index.html", {"request": request})

@router.post("")
async def sentiment(json: InputData):
    output = pipeline(task = 'sentiment-analysis',
                      model = model_name)(json.input_data)[0]
    output['input_data'] = json.input_data
    return output

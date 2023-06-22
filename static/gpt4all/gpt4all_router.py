from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from transformers import pipeline
from pydantic import BaseModel, Field
from gpt4all import GPT4All
import pdb

templates = Jinja2Templates(directory="templates")
router = APIRouter()

class InputData(BaseModel):
    input_data: str = Field(..., min_length=1, description="Input data must be at least 1 character long")

gptj = GPT4All("ggml-gpt4all-j-v1.3-groovy")


@router.get("")
async def gpt4all(request: Request):
    return templates.TemplateResponse("gpt4all.html", {
        "request": request })

@router.post("")
async def gpt4all(json: InputData):
    user_input = json.input_data

    messages = [{ "role": "user", "content": user_input }]
    resp = gptj.chat_completion(messages)

    return resp['choices'][0]['message']['content']

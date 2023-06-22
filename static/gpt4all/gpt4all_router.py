from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from transformers import pipeline
from pydantic import BaseModel, Field
from gpt4all import GPT4All
import pdb

templates = Jinja2Templates(directory="static/gpt4all")
router = APIRouter()

class InputData(BaseModel):
    input_data: str = Field(..., min_length=1, description="Input data must be at least 1 character long")

gptj = GPT4All("ggml-gpt4all-j-v1.3-groovy")



@router.get("")
async def semantic(request: Request):
    # pdb.set_trace() # for debugging
    return templates.TemplateResponse("index.html", {
        "request": request })

@router.post("")
async def semantic(json: InputData):
    my_input = json.input_data

    messages = [{"role": "user", "content": "Name 3 colors"}]
    resp = gptj.chat_completion(messages)

    pdb.set_trace()
    return "output"

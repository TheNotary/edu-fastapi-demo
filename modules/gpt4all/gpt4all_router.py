import os
from fastapi import APIRouter, Request
from helpers.jinja_helpers import build_templates_and_router
from transformers import pipeline
from pydantic import BaseModel, Field
from gpt4all import GPT4All

templates, router, module_name = build_templates_and_router(__file__)
gptj = None

class InputData(BaseModel):
    input_data: str = Field(..., min_length=1, description="Input data must be at least 1 character long")

@router.get("")
async def gpt4all(request: Request):
        return templates.TemplateResponse("modules/" + module_name + "/index.html", {"request": request})

@router.post("")
async def gpt4all(json: InputData):
    global gptj
    if gptj == None:
      gptj = GPT4All("ggml-gpt4all-j-v1.3-groovy")

    user_input = json.input_data

    messages = [{ "role": "user", "content": user_input }]
    resp = gptj.chat_completion(messages)

    return resp['choices'][0]['message']['content']

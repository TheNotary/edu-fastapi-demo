from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from llama_cpp import Llama

import pdb

templates = Jinja2Templates(directory="templates")
router = APIRouter()

class InputData(BaseModel):
    input_data: str = Field(..., min_length=1, description="Input data must be at least 1 character long")

llm = Llama(model_path="./wizardlm-30b-uncensored.ggmlv3.q6_K.bin")
output = llm("Q: Name the planets in the solar system? A: ", max_tokens=64, stop=["Q:", "\n"], echo=True)
print(output)

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

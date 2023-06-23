from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from llama_cpp import Llama

import pdb

llm = None
templates = Jinja2Templates(directory="templates")
router = APIRouter()

class InputData(BaseModel):
    input_data: str = Field(..., min_length=1, description="Input data must be at least 1 character long")


@router.get("")
async def wizard_lm(request: Request):
    return templates.TemplateResponse("wizard_lm.html", {
        "request": request })

@router.post("")
async def wizard_lm(json: InputData):
    global llm
    if llm == None:
      llm = Llama(model_path="./wizardlm-30b-uncensored.ggmlv3.q6_K.bin")

    user_input = json.input_data # "Q: Name the planets in the solar system? A: "

    resp = llm(user_input, max_tokens=512, stop=["Q:", "\n"], echo=True)

    return resp['choices'][0]['text']

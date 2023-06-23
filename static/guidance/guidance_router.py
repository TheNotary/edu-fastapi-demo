from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

import pdb

templates = Jinja2Templates(directory="templates")
router = APIRouter()

class InputData(BaseModel):
    input_data: str = Field(..., min_length=1, description="Input data must be at least 1 character long")




@router.get("")
async def guidance(request: Request):
    return templates.TemplateResponse("guidance.html", {
        "request": request })

@router.post("")
async def guidance(json: InputData):
    user_input = json.input_data

    # messages = [{ "role": "user", "content": user_input }]
    # resp = gptj.chat_completion(messages)

    return resp['choices'][0]['message']['content']

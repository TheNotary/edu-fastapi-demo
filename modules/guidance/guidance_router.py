from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from helpers.jinja_helpers import build_templates_and_router
import guidance

templates, router, module_name = build_templates_and_router(__file__)

llm = guidance.llms.Transformers("wizardlm-30b-uncensored.ggmlv3.q6_K.bin", device=0)

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

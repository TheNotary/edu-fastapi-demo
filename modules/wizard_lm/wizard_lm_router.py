from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import List, Optional
from llama_cpp import Llama
from helpers.jinja_helpers import build_templates_and_router

llm = None
templates, router, module_name = build_templates_and_router(__file__)

class Message(BaseModel):
    role: str = Field(..., description="The role of the message sender, typically 'user' or 'assistant'")
    content: str = Field(..., min_length=1, description="The content of the message")

class OpenAiInputData(BaseModel):
    model: str = Field(..., description="The model to use for text generation")
    temperature: Optional[float] = Field(None, description="Controls randomness in the model's output")
    max_tokens: Optional[int] = Field(None, description="The maximum number of tokens in the model's output")
    messages: List[Message] = Field(..., description="List of message objects")

class InputData(BaseModel):
    input_data: str = Field(..., min_length=1, description="Input data must be at least 1 character long")

@router.get("")
async def wizard_lm(request: Request):
    return templates.TemplateResponse("modules/" + module_name + "/index.html", {"request": request})

@router.post("")
async def wizard_lm(json: InputData):
    global llm
    if llm == None:
      llm = Llama(model_path="./wizardlm-30b-uncensored.ggmlv3.q6_K.bin")

    user_input = json.input_data # "Q: Name the planets in the solar system? A: "

    resp = llm(user_input, max_tokens=512, stop=["Q:", "\n"], echo=True)

    return resp['choices'][0]['text']

@router.post("/oai")
async def wizard_lm_oai(json: OpenAiInputData):
    global llm
    if llm == None:
      llm = Llama(model_path="./wizardlm-30b-uncensored.ggmlv3.q6_K.bin",
                  n_ctx=512)

    user_input = json.messages[0].content

    resp = llm(user_input,
               max_tokens=500,
               temperature=0,
               stop=["Q:", "\n"],
               echo=True)

    correctResponse = {
        'choices': [
            {
                'message': {
                    'content': resp['choices'][0]['text']
                }
            }
        ]
    }

    return correctResponse

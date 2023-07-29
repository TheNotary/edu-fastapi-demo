from fastapi import Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional
import pdb

import torch
from helpers.jinja_helpers import build_templates_and_router

from transformers import AutoTokenizer, pipeline, logging
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
import argparse

llm = None
templates, router, module_name = build_templates_and_router(__file__)

model_basename = "TheBloke/starcoder-GPTQ"
use_triton = False
tokenizer = AutoTokenizer.from_pretrained(model_basename, use_fast=True)

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
async def starcoder_gptq(request: Request):
    return templates.TemplateResponse("modules/" + module_name + "/index.html", {"request": request})

@router.post("")
async def starcoder_gptq(json: InputData):
    global llm
    if llm == None:
        llm = AutoGPTQForCausalLM.from_quantized(model_basename,
            use_safetensors=True,
            trust_remote_code=True,
            device="cuda:0",
            use_triton=use_triton,
            quantize_config=None)

    user_input = json.input_data # "Q: Name the planets in the solar system? A: "

    user_input = '''
<fim_prefix>
// A javascript function
<fim_suffix>
function printHelloWorld() {
<fim_middle>
}
    '''

    # inputs = tokenizer.encode(user_input, return_tensors="pt").to(llm.device)

    outputs = tokenizer.decode(llm.generate(**tokenizer(user_input, return_tensors="pt").to(llm.device),
                                            max_new_tokens=40,
                                            labels=["}"] )[0])

    pdb.set_trace()

    # outputs = llm.generate(inputs)
    # print(tokenizer.decode(outputs[0]))
    # resp = llm(user_input, max_tokens=512, stop=["Q:", "\n"], echo=True)

    return outputs

@router.post("/oai")
async def starcoder_gptq_oai(json: OpenAiInputData):
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

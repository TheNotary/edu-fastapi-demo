from fastapi import Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional
import pdb

from helpers.jinja_helpers import build_templates_and_router

from transformers import AutoTokenizer, pipeline, logging
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig

model = None
templates, router, module_name = build_templates_and_router(__file__)

model_basename = "TheBloke/starcoder-GPTQ"
use_triton = False
tokenizer = AutoTokenizer.from_pretrained(model_basename, use_fast=True)

class InputData(BaseModel):
    input_data: str = Field(..., min_length=1, description="Input data must be at least 1 character long")

@router.get("")
async def starcoder_gptq(request: Request):
    return templates.TemplateResponse("modules/" + module_name + "/index.html", {"request": request})

@router.post("")
async def starcoder_gptq(json: InputData):
    global model
    if model == None:
        model = AutoGPTQForCausalLM.from_quantized(model_basename,
            use_safetensors=True,
            trust_remote_code=True,
            device="cuda:0",
            use_triton=use_triton,
            quantize_config=None)

    user_input = json.input_data # "Q: Name the planets in the solar system? A: "

    user_input = '''
// A javascript function
function printHelloWorld() {
    '''

    inputs = tokenizer(user_input, return_tensors="pt").to(model.device)
    embedding = model.generate(**inputs,
                             max_new_tokens=40,
                             labels=["}"] )[0]

    outputs = tokenizer.decode(embedding)
    return outputs

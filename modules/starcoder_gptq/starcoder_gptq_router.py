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

    starting_input = "A javascript function that prints hello world"
    commentized_input = commentize_input(starting_input)
    function_name = choose_function_name(commentized_input)

    templated_input = f"""<fim_prefix>
{commentized_input}
function {function_name}() {{
<fim_suffix>
}}
<fim_middle>
"""

    raw_output = perform_inferance(templated_input)
    middle = extract_middle(raw_output)
    pdb.set_trace()

    formatted_code = format_code(templated_input, middle)
    return formatted_code

def perform_inferance(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    embedding = model.generate(**inputs,
                             max_new_tokens=40 )[0]

    return tokenizer.decode(embedding)

def commentize_input(starting_input):
    return f'// {starting_input}'

def choose_function_name(commentized_input):
    subpromt = f"""<fim_prefix>
{commentized_input}
function
<fim_suffix>
() {{
<fim_middle>
"""
    inference = perform_inferance(subpromt)
    middle = extract_middle(inference)
    return "printHelloWorld"

def extract_middle(raw_output):
    try:
        return raw_output.split('<fim_middle>\n')[1].split('<|endoftext|>')[0]
    except IndexError:
        return "Unable to find text between <fim_middle> and '<|endoftext|>' "

def format_code(templated_input, middle):
    return templated_input.replace("<fim_middle>", "").replace("<fim_prefix>", "").replace("<fim_suffix>", middle)


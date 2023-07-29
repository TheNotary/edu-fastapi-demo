from fastapi import FastAPI, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from transformers import pipeline
from pydantic import BaseModel, Field

from helpers.jinja_helpers import build_templates

# Module Controllers
from modules.sentiment.sentiment_router import router as sentiment_router
from modules.gpt4all.gpt4all_router import router as gpt4all_router
from modules.wizard_lm.wizard_lm_router import router as wizard_lm_router
from modules.basics.basics_router import router as basics_router
from modules.speech_t5.speech_t5_router import router as speech_t5_router
from modules.guidance.guidance_router import router as guidance_router
from modules.starcoder_gptq.starcoder_gptq_router import router as starcoder_gptq_router

app = FastAPI()
templates = build_templates()
app.mount("/modules", StaticFiles(directory="./modules"), name="modules")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("layout/home.html", {"request": request})

app.include_router(basics_router, prefix="/basics")
app.include_router(sentiment_router, prefix="/sentiment")
app.include_router(gpt4all_router, prefix="/gpt4all")
app.include_router(wizard_lm_router, prefix="/wizard_lm")
app.include_router(speech_t5_router, prefix="/speech_t5")
app.include_router(guidance_router, prefix="/guidance")
app.include_router(starcoder_gptq_router, prefix="/starcoder_gptq")

# @app.post("/gptj")
# async def ml(json: InputData):
#     output = pipeline(task = 'sentiment-analysis',
#                       model = model_name)(json.input_data)[0]
#     output['input_data'] = json.input_data
#     return output

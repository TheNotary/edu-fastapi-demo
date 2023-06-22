from fastapi import FastAPI, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from transformers import pipeline
from pydantic import BaseModel, Field

from static.semantic.semantic_router import router as semantic_router
from static.gpt4all.gpt4all_router import router as gpt4all_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/basics")
async def basics(request: Request):
    return templates.TemplateResponse("basics.html", {"request": request})

@app.get("/hello")
async def hello_world(name: str = Query(..., min_length=1, max_length=50, description="Your name")):
    return {"message": f"Hello, {name}!"}

app.include_router(semantic_router, prefix="/semantic")
app.include_router(gpt4all_router, prefix="/gpt4all")

# @app.post("/gptj")
# async def ml(json: InputData):
#     output = pipeline(task = 'sentiment-analysis',
#                       model = model_name)(json.input_data)[0]
#     output['input_data'] = json.input_data
#     return output

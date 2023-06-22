from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from transformers import pipeline
from pydantic import BaseModel, Field

from static.semantic.semantic_router import router as semantic_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")

@app.get("/")
def read_root():
    return RedirectResponse(url='/static/index.html')

@app.get("/hello")
async def hello_world(name: str = Query(..., min_length=1, max_length=50, description="Your name")):
    return {"message": f"Hello, {name}!"}

app.include_router(semantic_router, prefix="/semantic")

# @app.post("/gptj")
# async def ml(json: InputData):
#     output = pipeline(task = 'sentiment-analysis',
#                       model = model_name)(json.input_data)[0]
#     output['input_data'] = json.input_data
#     return output

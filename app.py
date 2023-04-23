from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
async def hello_world(name: str = Query(..., min_length=1, max_length=50, description="Your name")):
    return {"message": f"Hello, {name}!"}

@app.get("/ml")
async def ml(input: str = Query(..., min_length=1, max_length=300, description="Phrase to apply an ML model to")):

    return {"message": f"Hello, {input}!"}

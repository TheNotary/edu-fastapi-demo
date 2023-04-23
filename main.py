from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
async def hello_world(name: str = Query(..., min_length=1, max_length=50, description="Your name")):
    return {"message": f"Hello, {name}!"}

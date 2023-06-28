from fastapi import Query, Request
from pydantic import BaseModel, Field
from helpers.jinja_helpers import build_templates_and_router
import pdb

# This is the controller for the 'basics' modules.  The basics module doesn't
# really demo anything interesting about datascience, it's really just a
# cheap hello world to FastAPI.

llm = None
templates, router, module_name = build_templates_and_router(__file__)

# 1
class InputData(BaseModel):
    input_data: str = Field(..., min_length=1, description="Input data must be at least 1 character long")
# 2
@router.get("")
async def basics(request: Request):
    # pdb.set_trace() # for debugging
    return templates.TemplateResponse("static/" + module_name + "/index.html", {"request": request})
# 3
@router.get("/hello")
async def hello_world(name: str = Query(..., min_length=1, max_length=50, description="Your name")):
    return {"message": f"Hello, {name}!"}
# 4
@router.post("/hello")
async def hello_world(name: str = Query(..., min_length=1, max_length=50, description="Your name")):
    return {"message": f"Hello, {name}!"}

# 1
# This class is how we define our API input formats.  It's something that
# makes FastAPI standup as pretty handy since it builds in a little bit
# of input validation without it being much work

# 2
# This is where we setup the simple get route for this module.  ie, when
# a GET request for localhost:8000/basics comes in, this code fires.
# The response to the request is to serve the /templates/basics.html jinja template

# 3
# Here we're showing a simple way of passing data into our api using query params.
# Using the get verb in this way is educational, you can manually invoke this endpoint
# by navigating to localhost:8000/basics/hello?name=john in a web browser
# ...but this is NOT a good practice because as a convention, the GET verb
# shouldn't perform API operations --instead POST should do that kind of stuff.

# 4
# This is better, but I ran out of time to...
# TODO: make it proper json as the input and write a curl example

import os
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
import psutil

def has_file(filename):
    return os.path.isfile(os.path.join('./' + filename))

def build_templates():
    templates = Jinja2Templates(directory=".")
    templates.env.globals['has_file'] = has_file
    templates.env.globals['ram'] = int(psutil.virtual_memory().total / 10**9)
    return templates

# This function just hides a bunch of boilerplate that emerges from FastAPI
def build_templates_and_router(file_name):
    templates = build_templates()
    router = APIRouter()
    module_name = os.path.basename(file_name).replace("_router.py", "")

    return [templates, router, module_name]

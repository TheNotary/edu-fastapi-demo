import os
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter


def has_file(filename):
    return os.path.isfile(os.path.join('./' + filename))

def build_templates():
    templates = Jinja2Templates(directory="templates")
    templates.env.globals['has_file'] = has_file
    return templates

def build_templates_and_router():
    templates = build_templates()
    router = APIRouter()
    return [templates, router]

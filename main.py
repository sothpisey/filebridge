from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from urllib.parse import quote
import json
from routers import folder_structure
from routers import download

app = FastAPI()

app.include_router(folder_structure.router, prefix='/api', tags=['API'])
app.include_router(download.router, prefix='/api', tags=['API'])


with open('config.json', 'r') as file:
    data = json.load(file)
BASE_DIR = Path(data['path'])


app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@app.get('/', response_class=HTMLResponse)
def list_files(request: Request):

    return templates.TemplateResponse('index.html', {'request': request})
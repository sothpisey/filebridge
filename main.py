from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from urllib.parse import quote
import json
from routers import folder_structure, download, authenticator
from typing import Annotated

app = FastAPI()

app.include_router(folder_structure.router, prefix='/api', tags=['API'])
app.include_router(download.router, prefix='/api', tags=['API'], dependencies=[Depends(authenticator.get_current_user)])
app.include_router(authenticator.router, tags=['OAuth2'])


with open('config.json', 'r') as file:
    data = json.load(file)
BASE_DIR = Path(data['path'])


app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@app.get('/', response_class=HTMLResponse)
def list_files(request: Request, token: Annotated[str, Depends(authenticator.get_current_user)]):

    return templates.TemplateResponse('index.html', {'request': request})
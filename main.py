from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from urllib.parse import quote
import json
from routers import folder_structure, download, authenticator
from typing import Annotated

app = FastAPI()

app.include_router(folder_structure.router, prefix='/api', tags=['API'], dependencies=[Depends(authenticator.get_current_user)])
app.include_router(download.router, prefix='/api', tags=['API'], dependencies=[Depends(authenticator.get_current_user)])
app.include_router(authenticator.router, tags=['OAuth2'])


with open('config.json', 'r') as file:
    data = json.load(file)
BASE_DIR = Path(data['path'])


app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@app.get('/', response_class=HTMLResponse)
def list_files(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc: HTTPException):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/login")
    return await request.app.default_exception_handler(request, exc)
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

# This is the default directory to serve files from; can be changed dynamically
with open('config.json', 'r') as file:
    data = json.load(file)
BASE_DIR = Path(data['path'])

# Mount static files for serving
app.mount('/static', StaticFiles(directory='static'), name='static')

# Set up templates directory for rendering HTML
templates = Jinja2Templates(directory='templates')

@app.get('/', response_class=HTMLResponse)
def list_files(request: Request):  # Make sure to include 'Request' in the parameters
    '''Return an HTML page listing all files in the selected directory.'''
    files = [str(file.relative_to(BASE_DIR)) for file in BASE_DIR.iterdir() if file.is_file() and file.name != 'desktop.ini']
    # folder paths
    folders = [folder for folder in BASE_DIR.iterdir() if folder.is_dir()]
    # URL-encode the folder paths
    encoded_folders = [quote(str(item)) for item in BASE_DIR.iterdir() if item.is_dir()]
    parent_dir = quote(str(BASE_DIR.parent))

    # Render the HTML using the Jinja2 template, passing the request object
    return templates.TemplateResponse('index.html', {
        'request': request,
        'files': files,
        'folders': folders,
        'encoded_folders': encoded_folders,
        'zip': zip,
        'parent_dir': parent_dir,
        'BASE_DIR': BASE_DIR
    })
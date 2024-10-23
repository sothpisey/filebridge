from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

# This is the default directory to serve files from; can be changed dynamically
BASE_DIR = Path('C:/Users/TUF/Pictures/Screenshots')

# Mount static files for serving
app.mount('/static', StaticFiles(directory='static'), name='static')

# Set up templates directory for rendering HTML
templates = Jinja2Templates(directory='templates')

@app.get('/', response_class=HTMLResponse)
def list_files(request: Request):  # Make sure to include 'Request' in the parameters
    '''Return an HTML page listing all files in the selected directory.'''
    files = [str(file.relative_to(BASE_DIR)) for file in BASE_DIR.iterdir() if file.is_file() and file.name != 'desktop.ini']
    folders = [folder for folder in BASE_DIR.iterdir() if folder.is_dir()]

    # Render the HTML using the Jinja2 template, passing the request object
    return templates.TemplateResponse('index.html', {'request': request, 'files': files, 'folders': folders})

@app.get('/download/{file_name}')
def download_file(file_name: str):
    '''Download a file from the specified directory.'''
    file_path = BASE_DIR / file_name
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path, media_type='application/octet-stream', filename=file_name)
    raise HTTPException(status_code=404, detail='File not found')

@app.get('/change-directory/{new_dir}')
def change_directory(new_dir: str):
    '''Change the directory that the app serves files from.'''
    global BASE_DIR
    base_path = Path(new_dir)
    if base_path.exists() and base_path.is_dir():
        BASE_DIR = base_path
        return {'message': f'Serving files from {BASE_DIR}'}
    raise HTTPException(status_code=400, detail='Directory does not exist.')

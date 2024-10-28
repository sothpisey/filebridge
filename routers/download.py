from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from urllib.parse import quote, unquote
import json

# Read config file
with open('config.json', 'r') as file:
    data = json.load(file)

path = Path(data['path'])

router = APIRouter()


@router.get('/download/{file_name}')
def download_file(file_name: str):
    file_path = path / unquote(file_name)
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path, media_type='application/octet-stream', filename=file_path.name)
    raise HTTPException(status_code=404, detail='File not found')
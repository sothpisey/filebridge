from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pathlib import Path
from urllib.parse import quote, unquote
import json, zipfile, io

# Read config file
with open('config.json', 'r') as file:
    data = json.load(file)

path = Path(data['path'])

# Zip entire folder and return as buffer
def zip_folder(path: Path) -> io.BytesIO:
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in path.rglob('*'):
            if file.name != 'desktop.ini':
                zipf.write(file, arcname=file.relative_to(path))
    zip_buffer.seek(0)
    return zip_buffer

# Fastapi
router = APIRouter()

# File download endpoint
@router.get('/download/{file_name}')
def download_file(file_name: str):
    file_path = path / unquote(file_name)
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path, media_type='application/octet-stream', filename=file_path.name)
    raise HTTPException(status_code=404, detail='File not found')

# Download a full folder via the API in ZIP format
@router.get('/download-folder/{folder_path}')
def download_folder(folder_path: str):
    folder_path = Path(path / folder_path)
    if not folder_path.is_dir():
        raise HTTPException(status_code=404, detail="Directory not found")
    zip_file = zip_folder(folder_path)
    return StreamingResponse(zip_file, media_type='application/zip', headers={"Content-Disposition": f"attachment; filename={folder_path.name}.zip"})
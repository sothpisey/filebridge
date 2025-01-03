from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Union
from urllib.parse import quote
import json

router = APIRouter()

with open('config.json', 'r') as file:
    data =  json.load(file)
    

BASE_DIR = Path(data['path'])

class FileStructure(BaseModel):
    name: str
    type: str
    download_link: str
    children: List[Union["FileStructure", dict]] = []

FileStructure.update_forward_refs()

def create_folder_structure_json(path: Path, BASE_DIR: Path) -> FileStructure:
    def check_base_dir() -> str:
        if str(path.relative_to(BASE_DIR.absolute())) == '.':
            return '/'
        else:
            return '/api/download-folder/' + quote(str(path.relative_to(BASE_DIR.absolute())), safe='')
        
    result = {'name': path.name, 
              'type': 'folder', 
              'download_link': check_base_dir(), 
              'children': []
              }

    for entry in path.iterdir():
        if entry.is_dir():
            result['children'].append(create_folder_structure_json(entry, BASE_DIR))
        elif entry.name != 'desktop.ini':
            result['children'].append({
                'name': entry.name, 
                'type': 'file', 
                'download_link': '/api/download/' + quote(str(entry.relative_to(BASE_DIR.absolute())), safe='')
            })

    return result


@router.get("/folder-structure", response_model=FileStructure)
async def get_folder_structure():
    folder_structure = create_folder_structure_json(BASE_DIR, BASE_DIR)
    return folder_structure
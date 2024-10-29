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
    result = {'name': path.name, 'type': 'folder', 'download_link': 'None', 'children': []}

    if not path.is_dir():
        return result

    for entry in path.iterdir():
        if entry.is_dir():
            result['children'].append(create_folder_structure_json(entry, BASE_DIR))
        else:
            result['children'].append({
                'name': entry.name, 
                'type': 'file', 
                'download_link': '/api/download/' + quote(str(entry.relative_to(BASE_DIR.absolute())))
            })

    return result


@router.get("/folder-structure", response_model=FileStructure)
async def get_folder_structure():
    folder_structure = create_folder_structure_json(BASE_DIR, BASE_DIR)
    return folder_structure
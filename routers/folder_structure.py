from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Union
import json

router = APIRouter()

with open('config.json', 'r') as file:
    data =  json.load(file)
    

path = Path(data['path'])

class FileStructure(BaseModel):
    name: str
    type: str
    children: List[Union["FileStructure", dict]] = []

FileStructure.update_forward_refs()

def create_folder_structure_json(path: Path) -> FileStructure:
    result = {'name': path.name, 'type': 'folder', 'children': []}

    if not path.is_dir():
        return result

    for entry in path.iterdir():
        if entry.is_dir():
            result['children'].append(create_folder_structure_json(entry))
        else:
            result['children'].append({'name': entry.name, 'type': 'file'})

    return result


@router.get("/folder-structure", response_model=FileStructure)
async def get_folder_structure():
    folder_path = Path(path)
    folder_structure = create_folder_structure_json(folder_path)
    return folder_structure
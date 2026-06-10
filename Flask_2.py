from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
import logging
import random

app = FastAPI(title="Names API")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

allowed_names = ["Niko", "Promit", "Alex", "Anna"]

@app.get("/api/hello")
def say_hello(search: Optional[str] = Query(None)):
    """
    1. If 'search' query parameter is provided, filters and returns matching names.
    2. Otherwise, returns a single random name from the list.
    """
    if search:
        search_query = search.strip().lower()
        matched_names = [name for name in allowed_names if search_query in name.lower()]
        
        logger.info(f"Search query received: '{search_query}'. Matches found: {matched_names}")
        return {
            'search_term': search_query,
            'matches': matched_names,
            'count': len(matched_names)
        }

    if not allowed_names:
        return {'message': 'Hello world! No names are currently registered.'}
        
    random_name = random.choice(allowed_names)
    logger.info(f"Greeting picked: {random_name}")
    
    return {
        'message': f'Hello {random_name}',
        'current_pool': allowed_names
    }

@app.post("/api/names", status_code=201)
def add_name(payload: dict):
    """
    Adds a new name to the list. Expects JSON: {"name": "YourName"}
    """
    if 'name' not in payload:
        raise HTTPException(status_code=400, detail='Missing "name" field in request body')
        
    new_name = payload['name'].strip()
    if not new_name:
        raise HTTPException(status_code=400, detail='Name cannot be empty')
        
    if new_name in allowed_names:
        return {'message': f'{new_name} is already in the list!', 'names': allowed_names}

    allowed_names.append(new_name)
    return {'message': f'Successfully added {new_name}', 'names': allowed_names}

@app.delete("/api/names")
def delete_name(payload: dict):
    """
    Deletes a name from the list. Expects JSON: {"name": "YourName"}
    """
    if 'name' not in payload:
        raise HTTPException(status_code=400, detail='Missing "name" field in request body')
        
    target_name = payload['name'].strip()
    if target_name in allowed_names:
        allowed_names.remove(target_name)
        return {'message': f'Successfully deleted {target_name}', 'names': allowed_names}
        
    raise HTTPException(status_code=404, detail=f'Name "{target_name}" not found in the list.')

# http://127.0.0.1:5001/api/hello?search=ni
# http://127.0.0.1:5001/api/hello?search=xyz
# http://127.0.0.1:5001/api/hello
# fastapi dev Flask_2.py
from typing import Optional
from fastapi import FastAPI, File, Request, UploadFile, Response
from fastapi.responses import HTMLResponse
from .modules import imports
import os
import sys
import json
import math
from pathlib import Path
import ifcopenshell
import importlib.util


app = FastAPI()
UPLOAD_DIR = Path.cwd() / "app" / "temp"

def generate_html_response():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head> IFC File Upload</head>
        <body>
            
            <form method="post" action="/file/" enctype="multipart/form-data">
                <input type="file" name="file_upload" id="file_upload">
                <input type="submit" value="Upload IFC File" name="submit">
            </form>
            <iframe src="https://giphy.com/embed/IKeiU9lhqn6ZjTWDM3" width="480" height="360" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/zesprispain-IKeiU9lhqn6ZjTWDM3">via GIPHY</a></p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return generate_html_response()

    
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# simple fileupload
@app.post("/file/")
async def create_upload_file(file_upload: UploadFile):
    data = await file_upload.read()
    save_to = UPLOAD_DIR / file_upload.filename
    # File is saved in a temporary directory
    with open(save_to, "wb") as file_object:
        file_object.write(data)

    # Create a Rooms object with the uploaded file
    rooms = imports.Rooms(save_to)
    json = rooms.exportAsJson()
    return Response(content=json, media_type="application/json")
    

# file upload via webservice
@app.post("/uploadfile/")
async def create_upload_file(element1: UploadFile = File(...)):
    file = element1
    contents = await file.read()
    save_to = UPLOAD_DIR / file.filename
    with open(save_to, "wb") as file_object:
        file_object.write(contents)
    return {"filename": file.filename}


# print raw http-request for debugging purposes
@app.post("/debugging/")
async def show_request(request: Request):
    body = await request.body()
    print (body)
    return {"request": body}

# get walls by filename
@app.get("/project/{filename}/walls/")
async def get_walls(filename: str):
    if not filename.endswith(".ifc"):
        filename = filename + ".ifc"
    # handle url coding in filename
    filename = filename.replace("%20", " ")

    walls = imports.Walls(UPLOAD_DIR / filename)
    json =  walls.exportAsJson()
    return Response(content=json, media_type="application/json")

def load_modules():
    module_folder = Path.cwd() / "app" / "modules"
    load_modules = []
    for filename in os.listdir(module_folder):
        if filename.endswith(".py") and filename.startswith("_"):
            load_modules.append(filename[:-3])
            module_path = os.path.join(module_folder, filename)

            spec = importlib.util.spec_from_file_location(filename, module_path)
            module = importlib.util.module_from_spec(spec)
            module.imports = imports
            spec.loader.exec_module(module)

            load_modules.append(module)

    return load_modules

@app.get("/project/{filename}/items/")
async def get_items(filename: str):
    ifc_file = ifcopenshell.open(UPLOAD_DIR / filename)
    modules = load_modules()
    results = []
    for module in modules:
        if(hasattr(module, "run")):
            results.append(module.run(ifc_file))

    return results

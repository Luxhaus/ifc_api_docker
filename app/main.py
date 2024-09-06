from typing import Optional
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import HTMLResponse
from .modules.Rooms import Rooms
from .modules.Walls import Walls
from pathlib import Path

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
    rooms = Rooms(save_to)
    json = rooms.exportAsJson()
    return Response(content=json, media_type="application/json")
    

# file upload via webservice
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    save_to = UPLOAD_DIR / file.filename
    with open(save_to, "wb") as file_object:
        file_object.write(contents)
    return {"filename": file.filename}

# get rooms by filename
@app.get("{filename}/rooms/")
async def get_rooms(filename: str):
    rooms = Rooms(UPLOAD_DIR / filename)
    return rooms.exportAsJson()

# get walls by filename
@app.get("/project/{filename}/walls/")
async def get_walls(filename: str):
    if not filename.endswith(".ifc"):
        filename = filename + ".ifc"
    # handle url coding in filename
    filename = filename.replace("%20", " ")

    walls = Walls(UPLOAD_DIR / filename)
    json =  walls.exportAsJson()
    return Response(content=json, media_type="application/json")
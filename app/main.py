from typing import Optional
from fastapi import FastAPI, UploadFile, Response
from fastapi.responses import HTMLResponse
from .modules.Rooms import Rooms
from pathlib import Path

app = FastAPI()
UPLOAD_DIR = Path.cwd() / "app" / "temp"

def generate_html_response():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head> IFC File Upload</head>

        <body>
            <h1>IFC File Upload</h1>
            <form method="post" action="/file/" enctype="multipart/form-data">
                <input type="file" name="file_upload" id="file_upload">
                <input type="submit" value="Upload IFC File" name="submit">
            </form>
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
    


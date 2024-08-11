import logging
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import json
from pathlib import Path

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HISTORY_FILE = "history.json"
DATA_FILE = "data.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {"file_list": [], "source_folder": [], "destination_folder": [], "tags": []}

def save_history(history):
    history["file_list"] = list(dict.fromkeys(history["file_list"]))  # Remove duplicates
    history["source_folder"] = list(dict.fromkeys(history["source_folder"]))  # Remove duplicates
    history["destination_folder"] = list(dict.fromkeys(history["destination_folder"]))  # Remove duplicates
    history["tags"] = list(dict.fromkeys(history["tags"]))  # Remove duplicates
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# Function to update the history with a new entry
def update_history(field_name, new_entry):
    history = load_history()  # Load the existing history

    if new_entry not in history[field_name]:  # Avoid duplicates
        history[field_name].append(new_entry)  # Add the new entry to the appropriate field
        save_history(history)  # Save the updated history


@app.post("/update-history")
async def update_history_endpoint(request: Request):
    data = await request.json()
    field_name = data['field_name']
    new_entry = data['new_entry']

    update_history(field_name, new_entry)
    return {"status": "success"}

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    history = load_history()
    return templates.TemplateResponse("index.html", {"request": request, "history": history})

@app.post("/list-files", response_class=JSONResponse)
async def list_files(folder_path: str = Form(...)):
    if not os.path.exists(folder_path):
        return JSONResponse(content={"error": "Folder not found"}, status_code=404)
    
    files = [{"filename": file} for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    return JSONResponse(content={"files": files})


@app.post("/generate-json-list", response_class=HTMLResponse)
async def generate_json_list(request: Request, folder_path: str = Form(...), file_list: str = Form(...), destination_folder: str = Form(...)):
    logger.info(f"Received folder_path: {folder_path}")
    logger.info(f"Received destination_folder: {destination_folder}")
    logger.info(f"Received file_list: {file_list}")

    # Split the file list by new lines and remove any empty lines
    files = [file.strip() for file in file_list.split("\n") if file.strip()]
    file_data = [{"filename": os.path.basename(file), "filepath": file} for file in files]

    # Validate that files are not empty
    if not files:
        logger.error("No valid files found in the file list.")
        return HTMLResponse(content="No valid files found in the file list.", status_code=400)

    # Ensure the destination folder exists
    if not os.path.isdir(destination_folder):
        logger.error(f"The specified destination folder does not exist or is not a directory: {destination_folder}")
        return HTMLResponse(content="The specified destination folder does not exist or is not a directory.", status_code=400)

    # Define the path where the JSON file will be created
    json_file_path = os.path.join(destination_folder, "file_list.json")
    logger.info(f"File list path to be created: {json_file_path}")

    # Write the file list to the JSON file
    try:
        with open(json_file_path, "w") as f:
            json.dump({"files": file_data}, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to write the JSON file: {e}")
        return HTMLResponse(content=f"Failed to write the JSON file: {e}", status_code=500)

    message = f"File list generated successfully at {json_file_path}"
    logger.info(message)

    # Return to the index page with a success message
    return templates.TemplateResponse("index.html", {"request": request, "message": message})

@app.get("/tags", response_class=JSONResponse)
async def get_tags():
    tags_file = BASE_DIR / "tags.json"
    if os.path.exists(tags_file):
        with open(tags_file, "r") as f:
            tags = json.load(f).get("tags", [])
    else:
        tags = []
    return JSONResponse(content=tags)

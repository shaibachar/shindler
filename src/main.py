from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

HISTORY_FILE = "history.json"
FILE_UPDATES_FILE = "file_updates.json"
TAGS_FILE = "tags.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {"file_list": [], "source_folder": [], "destination_folder": []}

def save_history(history):
    history["file_list"] = list(dict.fromkeys(history["file_list"]))  # Remove duplicates
    history["source_folder"] = list(dict.fromkeys(history["source_folder"]))  # Remove duplicates
    history["destination_folder"] = list(dict.fromkeys(history["destination_folder"]))  # Remove duplicates
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def validate_files(file_list, destination_folder):
    missing_files = []
    for file_info in file_list:
        if not os.path.exists(os.path.join(destination_folder, file_info["filename"])):
            missing_files.append(file_info["filename"])
    return missing_files

def copy_files(file_list_path, source_folder, destination_folder):
    if not os.path.exists(file_list_path):
        raise FileNotFoundError(f"File list '{file_list_path}' not found!")

    if not os.path.exists(source_folder):
        raise FileNotFoundError(f"Source folder '{source_folder}' not found!")

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    with open(file_list_path, "r") as f:
        file_list = json.load(f)["files"]

    copied_files_count = 0
    for file_info in file_list:
        filename = file_info["filename"]
        source_path = os.path.join(source_folder, filename)
        destination_path = os.path.join(destination_folder, filename)
        if os.path.exists(source_path):
            shutil.copy2(source_path, destination_path)
            copied_files_count += 1
        else:
            print(f"File '{filename}' not found in '{source_folder}'")

    missing_files = validate_files(file_list, destination_folder)
    return copied_files_count, missing_files

def generate_file_list(folder_path):
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder '{folder_path}' not found!")
    
    files = [{"filename": file, "description": "", "tags": []} for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    
    file_list_path = os.path.join(folder_path, "file_list.json")
    with open(file_list_path, "w") as f:
        json.dump({"files": files}, f, indent=4)
    
    return file_list_path

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    history = load_history()
    return templates.TemplateResponse("index.html", {"request": request, "history": history})

@app.post("/copy-files", response_class=HTMLResponse)
async def copy_files_endpoint(request: Request, file_list: str = Form(...), source_folder: str = Form(...), destination_folder: str = Form(...)):
    try:
        copied_files_count, missing_files = copy_files(file_list, source_folder, destination_folder)
        message = f"Copying process completed. {copied_files_count} files copied."
        if missing_files:
            message += f" Missing files in destination: {', '.join(missing_files)}"
    except FileNotFoundError as e:
        message = str(e)
    
    history = load_history()
    if file_list not in history["file_list"]:
        history["file_list"].append(file_list)
    if source_folder not in history["source_folder"]:
        history["source_folder"].append(source_folder)
    if destination_folder not in history["destination_folder"]:
        history["destination_folder"].append(destination_folder)
    save_history(history)
    
    return templates.TemplateResponse("index.html", {"request": request, "message": message, "history": history, "file_list": file_list, "source_folder": source_folder, "destination_folder": destination_folder})

@app.post("/validate-destination", response_class=HTMLResponse)
async def validate_destination_endpoint(request: Request, file_list: str = Form(...), destination_folder: str = Form(...)):
    try:
        with open(file_list, "r") as f:
            file_list_data = json.load(f)["files"]
        missing_files = validate_files(file_list_data, destination_folder)
        if missing_files:
            message = f"Missing files in destination: {', '.join(missing_files)}"
        else:
            message = "All files are present in the destination folder."
    except FileNotFoundError as e:
        message = str(e)
    
    history = load_history()
    if file_list not in history["file_list"]:
        history["file_list"].append(file_list)
    if destination_folder not in history["destination_folder"]:
        history["destination_folder"].append(destination_folder)
    save_history(history)
    
    return templates.TemplateResponse("index.html", {"request": request, "message": message, "history": history, "file_list": file_list, "destination_folder": destination_folder})

@app.post("/generate-file-list", response_class=HTMLResponse)
async def generate_file_list_endpoint(request: Request, folder_path: str = Form(...)):
    try:
        file_list_path = generate_file_list(folder_path)
        message = f"File list generated successfully at {file_list_path}"
    except FileNotFoundError as e:
        message = str(e)
    
    history = load_history()
    if folder_path not in history["source_folder"]:
        history["source_folder"].append(folder_path)
    save_history(history)
    
    return templates.TemplateResponse("index.html", {"request": request, "message": message, "history": history, "folder_path": folder_path})

@app.get("/manage-files", response_class=HTMLResponse)
async def manage_files():
    if not os.path.exists(FILE_UPDATES_FILE):
        with open(FILE_UPDATES_FILE, "w") as f:
            json.dump({}, f, indent=4)
    return FileResponse(FILE_UPDATES_FILE)

@app.get("/manage-tags", response_class=HTMLResponse)
async def manage_tags():
    if not os.path.exists(TAGS_FILE):
        with open(TAGS_FILE, "w") as f:
            json.dump({"tags": []}, f, indent=4)
    return FileResponse(TAGS_FILE)

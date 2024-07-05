import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import json
import shutil

HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {"file_list": [], "source_folder": [], "destination_folder": []}

def save_history(file_list_history, source_folder_history, destination_folder_history):
    history = {
        "file_list": list(file_list_history),
        "source_folder": list(source_folder_history),
        "destination_folder": list(destination_folder_history)
    }
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def update_history(entry, history):
    value = entry.get()
    if value not in history:
        history.insert(0, value)
    if len(history) > 10:  # Keep only the last 10 entries
        history.pop()

def load_file_list(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File list '{file_path}' not found!")
    
    with open(file_path, "r") as f:
        file_list_data = json.load(f)
        num_files = len(file_list_data.get("files", []))
    return num_files

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

def validate_destination(file_list_path, destination_folder):
    if not os.path.exists(file_list_path):
        raise FileNotFoundError(f"File list '{file_list_path}' not found!")

    if not os.path.exists(destination_folder):
        raise FileNotFoundError(f"Destination folder '{destination_folder}' not found!")

    with open(file_list_path, "r") as f:
        file_list = json.load(f)["files"]

    missing_files = validate_files(file_list, destination_folder)
    return missing_files

# GUI Setup
root = tk.Tk()
root.title("File Copy Script")
root.geometry("800x300")

style = ttk.Style()
style.configure("TLabel", font=("Arial", 10))
style.configure("TButton", font=("Arial", 10))

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

history = load_history()
file_list_history = history["file_list"]
source_folder_history = history["source_folder"]
destination_folder_history = history["destination_folder"]

def create_combobox(entry, history, command=None):
    combobox = ttk.Combobox(main_frame, values=history, width=47)
    combobox.grid(row=entry.grid_info()['row'], column=1, padx=10, pady=10)
    combobox.bind("<<ComboboxSelected>>", lambda e: entry.delete(0, tk.END) or entry.insert(0, combobox.get()) or (command and command(combobox.get())))
    return combobox

def select_file():
    file_path = filedialog.askopenfilename(title="Select file list", filetypes=[("JSON files", "*.json")])
    file_list_entry.delete(0, tk.END)
    file_list_entry.insert(0, file_path)
    try:
        num_files = load_file_list(file_path)
        statistics_label.config(text=f"Number of files listed: {num_files}")
    except FileNotFoundError as e:
        messagebox.showerror("Error", str(e))

def select_folder(entry):
    folder_path = filedialog.askdirectory(title="Select folder")
    entry.delete(0, tk.END)
    entry.insert(0, folder_path)

def manage_files():
    if not os.path.exists("file_updates.json"):
        with open("file_updates.json", "w") as f:
            json.dump({}, f, indent=4)
    os.system("notepad file_updates.json")

def manage_tags():
    if not os.path.exists("tags.json"):
        with open("tags.json", "w") as f:
            json.dump({"tags": []}, f, indent=4)
    os.system("notepad tags.json")

def copy_files_command():
    file_list_path = file_list_entry.get()
    source_folder = source_folder_entry.get()
    destination_folder = destination_folder_entry.get()

    try:
        copied_files_count, missing_files = copy_files(file_list_path, source_folder, destination_folder)
        if missing_files:
            messagebox.showwarning("Validation", f"Missing files in destination: {', '.join(missing_files)}")
        else:
            messagebox.showinfo("Completed", f"Copying process completed. {copied_files_count} files copied.")
        update_history(file_list_entry, file_list_history)
        update_history(source_folder_entry, source_folder_history)
        update_history(destination_folder_entry, destination_folder_history)
        save_history(file_list_history, source_folder_history, destination_folder_history)
    except FileNotFoundError as e:
        messagebox.showerror("Error", str(e))

def validate_destination_command():
    file_list_path = file_list_entry.get()
    destination_folder = destination_folder_entry.get()

    try:
        missing_files = validate_destination(file_list_path, destination_folder)
        if missing_files:
            messagebox.showwarning("Validation", f"Missing files in destination: {', '.join(missing_files)}")
        else:
            messagebox.showinfo("Validation", "All files are present in the destination folder.")
    except FileNotFoundError as e:
        messagebox.showerror("Error", str(e))

ttk.Label(main_frame, text="File List:").grid(row=0, column=0, padx=10, pady=10)
file_list_entry = ttk.Entry(main_frame, width=50)
file_list_entry.grid(row=0, column=1, padx=10, pady=10)
file_list_combobox = create_combobox(file_list_entry, file_list_history, lambda file_path: statistics_label.config(text=f"Number of files listed: {load_file_list(file_path)}"))
ttk.Button(main_frame, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

statistics_label = ttk.Label(main_frame, text="Number of files listed: 0")
statistics_label.grid(row=0, column=3, padx=10, pady=10)

ttk.Label(main_frame, text="Source Folder:").grid(row=1, column=0, padx=10, pady=10)
source_folder_entry = ttk.Entry(main_frame, width=50)
source_folder_entry.grid(row=1, column=1, padx=10, pady=10)
create_combobox(source_folder_entry, source_folder_history)
ttk.Button(main_frame, text="Browse", command=lambda: select_folder(source_folder_entry)).grid(row=1, column=2, padx=10, pady=10)

ttk.Label(main_frame, text="Destination Folder:").grid(row=2, column=0, padx=10, pady=10)
destination_folder_entry = ttk.Entry(main_frame, width=50)
destination_folder_entry.grid(row=2, column=1, padx=10, pady=10)
create_combobox(destination_folder_entry, destination_folder_history)
ttk.Button(main_frame, text="Browse", command=lambda: select_folder(destination_folder_entry)).grid(row=2, column=2, padx=10, pady=10)

ttk.Button(main_frame, text="Manage File Updates", command=manage_files).grid(row=3, column=0, columnspan=3, pady=10)
ttk.Button(main_frame, text="Manage Tags", command=manage_tags).grid(row=4, column=0, columnspan=3, pady=10)

ttk.Button(main_frame, text="Copy Files", command=copy_files_command).grid(row=5, column=0, columnspan=2, pady=10)
ttk.Button(main_frame, text="Validate Destination", command=validate_destination_command).grid(row=5, column=2, columnspan=2, pady=10)

root.mainloop()

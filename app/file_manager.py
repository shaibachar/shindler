import os
import shutil
import json
import readline  # For tab completion
import rlcompleter  # To use the completer class
import platform

# Check if running on Windows and install pyreadline3 if necessary
if platform.system() == 'Windows':
    try:
        import pyreadline3
    except ImportError:
        print("pyreadline3 is not installed. Please install it using 'pip install pyreadline3'.")
        exit(1)

# Settings file path
SETTINGS_FILE = 'settings.json'

# Global variables for source, destination, and lists folders
global_settings = {
    "source_folder": None,
    "destination_folder": None,
    "lists_folder": None
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as file:
            settings = json.load(file)
            global_settings.update(settings)
            print("Settings loaded from settings.json")
    else:
        print("No settings file found. Using default settings.")

def save_settings():
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(global_settings, file, indent=4)
    print("Settings saved to settings.json")

def complete_path(text, state):
    line = readline.get_line_buffer().split()
    if not line:
        return [text + " "][state]
    else:
        cmd = line[0]
        if cmd in ["copy_list", "validate_list"] and global_settings['lists_folder']:
            lists_folder = global_settings['lists_folder']
            if os.path.isdir(lists_folder):
                options = [f for f in os.listdir(lists_folder) if f.startswith(text)]
                if state < len(options):
                    return options[state]
                else:
                    return None
        else:
            dirpath = os.path.expanduser(text)
            if not os.path.isdir(dirpath):
                dirpath = os.path.dirname(dirpath)
            if os.path.isdir(dirpath):
                options = [os.path.join(dirpath, f) + os.sep * (os.path.isdir(os.path.join(dirpath, f))) 
                           for f in os.listdir(dirpath) if f.startswith(os.path.basename(text))]
                if state < len(options):
                    return options[state]
                else:
                    return None

def copy_files(source_folder=None, destination_folder=None):
    source_folder = source_folder or global_settings['source_folder']
    destination_folder = destination_folder or global_settings['destination_folder']
    
    if not source_folder or not destination_folder:
        print("Source and destination folders must be set or provided.")
        return
    
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    for filename in os.listdir(source_folder):
        full_file_name = os.path.join(source_folder, filename)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, destination_folder)
    print(f"All files copied from {source_folder} to {destination_folder}")

def list_files_to_json(source_folder=None, destination_folder=None, json_filename="file_list.json"):
    source_folder = source_folder or global_settings['source_folder']
    destination_folder = destination_folder or global_settings['destination_folder']
    
    if not source_folder or not destination_folder:
        print("Source and destination folders must be set or provided.")
        return
    
    files = os.listdir(source_folder)
    files_list = [f for f in files if os.path.isfile(os.path.join(source_folder, f))]
    
    if global_settings['lists_folder']:
        json_file_path = os.path.join(global_settings['lists_folder'], json_filename)
    else:
        json_file_path = os.path.join(destination_folder, json_filename)
    
    if not os.path.exists(os.path.dirname(json_file_path)):
        os.makedirs(os.path.dirname(json_file_path))
    
    with open(json_file_path, 'w') as json_file:
        json.dump({"description": "File list", "file_list": files_list}, json_file, indent=4)
    
    print(f"File list saved to {json_file_path}")

def validate_files(source_folder=None, destination_folder=None):
    source_folder = source_folder or global_settings['source_folder']
    destination_folder = destination_folder or global_settings['destination_folder']
    
    if not source_folder or not destination_folder:
        print("Source and destination folders must be set or provided.")
        return
    
    source_files = set(os.listdir(source_folder))
    destination_files = set(os.listdir(destination_folder))
    missing_files = source_files - destination_files
    
    if missing_files:
        print(f"The following files are missing in the destination folder: {', '.join(missing_files)}")
    else:
        print("All files in the source folder are present in the destination folder.")

def copy_files_from_list(json_filename, source_folder=None, destination_folder=None):
    source_folder = source_folder or global_settings['source_folder']
    destination_folder = destination_folder or global_settings['destination_folder']
    
    if not source_folder or not destination_folder:
        print("Source and destination folders must be set or provided.")
        return
    
    if global_settings['lists_folder']:
        json_file_path = os.path.join(global_settings['lists_folder'], json_filename)
    else:
        json_file_path = json_filename
    
    if not os.path.exists(json_file_path):
        print(f"JSON file {json_file_path} not found.")
        return
    
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    file_list = data.get('file_list', [])
    
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    for filename in file_list:
        full_file_name = os.path.join(source_folder, filename)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, destination_folder)
            print(f"Copied {filename} to {destination_folder}")
        else:
            print(f"File {filename} not found in {source_folder}")

def validate_list(json_filename, source_folder=None):
    source_folder = source_folder or global_settings['source_folder']
    
    if not source_folder:
        print("Source folder must be set or provided.")
        return
    
    if global_settings['lists_folder']:
        json_file_path = os.path.join(global_settings['lists_folder'], json_filename)
    else:
        json_file_path = json_filename
    
    if not os.path.exists(json_file_path):
        print(f"JSON file {json_file_path} not found.")
        return
    
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    file_list = data.get('file_list', [])
    
    missing_files = [filename for filename in file_list if not os.path.isfile(os.path.join(source_folder, filename))]
    
    if missing_files:
        print(f"The following files listed in {json_filename} are missing in the source folder: {', '.join(missing_files)}")
    else:
        print(f"All files listed in {json_filename} are present in the source folder.")

def set_variable(variable, value):
    if variable in global_settings:
        global_settings[variable] = value
        print(f"{variable} set to {value}")
        save_settings()
    else:
        print(f"Unknown variable: {variable}")

def print_settings():
    print("Current settings:")
    for key, value in global_settings.items():
        print(f"{key}: {value if value else 'Not set'}")

def show_instructions():
    print("""
Hello! Welcome to File Manager.
You can use the following commands:
1. set - Set the source, destination, or lists folder
   Usage: set <source_folder|destination_folder|lists_folder> <path>
   
2. copy - Copy all files from source folder to destination folder
   Usage: copy [source_folder] [destination_folder]
   If no folders are provided, it will use the globally set ones.
   
3. list - List all files in source folder and save to a JSON file in the destination folder
   Usage: list [source_folder] [destination_folder] [json_filename]
   If no folders are provided, it will use the globally set ones.
   
4. validate - Validate that all files in the source folder exist in the destination folder
   Usage: validate [source_folder] [destination_folder]
   If no folders are provided, it will use the globally set ones.

5. copy_list - Copy files from source to destination based on a JSON file
   Usage: copy_list <json_filename>
   The JSON file will be searched in the lists_folder, and the operation will use the globally set source and destination folders.

6. validate_list - Validate that all files in the JSON list exist in the source folder
   Usage: validate_list <json_filename>
   The JSON file will be searched in the lists_folder, and the operation will use the globally set source folder.
   
7. settings - Print the current settings
   Usage: settings

8. menu - Print this menu again
   Usage: menu
   
Type your command below:
""")

def execute_command(command):
    parts = command.strip().split()
    if len(parts) == 0:
        print("No command entered. Please try again.")
        return
    
    cmd = parts[0]
    
    if cmd == 'set' and len(parts) == 3:
        set_variable(parts[1], parts[2])
    elif cmd == 'copy':
        if len(parts) == 3:
            copy_files(parts[1], parts[2])
        else:
            copy_files()
    elif cmd == 'list':
        if len(parts) == 4:
            list_files_to_json(parts[1], parts[2], parts[3])
        else:
            list_files_to_json()
    elif cmd == 'validate':
        if len(parts) == 3:
            validate_files(parts[1], parts[2])
        else:
            validate_files()
    elif cmd == 'copy_list':
        if len(parts) == 2:
            copy_files_from_list(parts[1])
        else:
            print("Usage: copy_list <json_filename>")
    elif cmd == 'validate_list':
        if len(parts) == 2:
            validate_list(parts[1])
        else:
            print("Usage: validate_list <json_filename>")
    elif cmd == 'settings':
        print_settings()
    elif cmd == 'menu':
        show_instructions()
    else:
        print("Invalid command or wrong number of arguments. Please try again.")

def main():
    # Load settings at startup
    load_settings()

    # Setup tab completion for paths
    readline.set_completer(complete_path)
    readline.parse_and_bind("tab: complete")

    show_instructions()
    
    while True:
        command = input("> ")
        if command.lower() in ['exit', 'quit']:
            print("Exiting File Manager. Goodbye!")
            break
        execute_command(command)

if __name__ == '__main__':
    main()

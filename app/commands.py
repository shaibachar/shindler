from settings import global_settings, save_settings
import os
import shutil
import json
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_success(message):
    print(Fore.GREEN + message)

def print_warning(message):
    print(Fore.YELLOW + message)

def print_error(message):
    print(Fore.RED + message)

def prompt_for_folder(folder_name):
    return input(f"Please provide the path for the {folder_name}: ")

def check_and_prompt_folders():
    if not global_settings['source_folder']:
        global_settings['source_folder'] = prompt_for_folder('source folder')
        save_settings()
    if not global_settings['destination_folder']:
        global_settings['destination_folder'] = prompt_for_folder('destination folder')
        save_settings()

    # Check if the destination folder exists, create it if it doesn't
    if not os.path.exists(global_settings['destination_folder']):
        os.makedirs(global_settings['destination_folder'])
        print_warning(f"The destination folder '{global_settings['destination_folder']}' did not exist and has been created.")

def copy_all_files(source_folder=None, destination_folder=None):
    check_and_prompt_folders()
    source_folder = source_folder or global_settings['source_folder']
    destination_folder = destination_folder or global_settings['destination_folder']
    
    for filename in os.listdir(source_folder):
        full_file_name = os.path.join(source_folder, filename)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, destination_folder)
    print_success(f"All files copied from {source_folder} to {destination_folder}")

def list_all_files_to_json(source_folder=None, destination_folder=None, json_filename="file_list.json"):
    check_and_prompt_folders()
    source_folder = source_folder or global_settings['source_folder']
    destination_folder = destination_folder or global_settings['destination_folder']
    
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
    
    print_success(f"File list saved to {json_file_path}")

def validate_all_files(source_folder=None, destination_folder=None):
    check_and_prompt_folders()
    source_folder = source_folder or global_settings['source_folder']
    destination_folder = destination_folder or global_settings['destination_folder']
    
    source_files = set(os.listdir(source_folder))
    destination_files = set(os.listdir(destination_folder))
    missing_files = source_files - destination_files
    
    if missing_files:
        print_warning(f"The following files are missing in the destination folder: {', '.join(missing_files)}")
    else:
        print_success("All files in the source folder are present in the destination folder.")

def copy_files_from_list(json_filename, source_folder=None, destination_folder=None):
    source_folder = source_folder or global_settings['source_folder']
    destination_folder = destination_folder or global_settings['destination_folder']
    
    if global_settings['lists_folder']:
        json_file_path = os.path.join(global_settings['lists_folder'], json_filename)
    else:
        json_file_path = json_filename
    
    if not os.path.exists(json_file_path):
        print_error(f"JSON file {json_file_path} not found.")
        return
    
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    file_list = data.get('file_list', [])
    
    for filename in file_list:
        full_file_name = os.path.join(source_folder, filename)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, destination_folder)
            print_success(f"Copied {filename} to {destination_folder}")
        else:
            print_warning(f"File {filename} not found in {source_folder}")

def validate_list(json_filename, source_folder=None, destination_folder=None):
    source_folder = source_folder or global_settings['source_folder']
    destination_folder = destination_folder or global_settings['destination_folder']
    
    if global_settings['lists_folder']:
        json_file_path = os.path.join(global_settings['lists_folder'], json_filename)
    else:
        json_file_path = json_filename
    
    if not os.path.exists(json_file_path):
        print_error(f"JSON file {json_file_path} not found.")
        return
    
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    file_list = set(data.get('file_list', []))
    
    # Check for missing files in the source folder
    missing_files = [filename for filename in file_list if not os.path.isfile(os.path.join(source_folder, filename))]
    
    if missing_files:
        print_warning(f"The following files listed in {json_filename} are missing in the source folder: {', '.join(missing_files)}")
    else:
        print_success(f"All files listed in {json_filename} are present in the source folder.")
    
    # Check for extra files in the destination folder
    if destination_folder:
        destination_files = set(os.listdir(destination_folder))
        extra_files = destination_files - file_list
        
        if extra_files:
            print_warning(f"Warning: The following files are in the destination folder but not listed in {json_filename}: {', '.join(extra_files)}")
        else:
            print_success(f"All files in the destination folder are accounted for in {json_filename}.")

def handle_copy_and_validate(command_parts):
    check_and_prompt_folders()
    source_folder = global_settings['source_folder']
    destination_folder = global_settings['destination_folder']
    
    # Copy each JSON list file specified before the "validate" command
    for part in command_parts:
        if part.lower() == 'validate':
            break
        copy_files_from_list(part, source_folder, destination_folder)
    
    # Validate all after copying
    if 'validate' in command_parts:
        for part in command_parts:
            if part.lower() == 'validate':
                continue
            validate_list(part, source_folder, destination_folder)

def set_variable(variable, value):
    if variable in global_settings:
        global_settings[variable] = value
        print_success(f"{variable} set to {value}")
        save_settings()
    else:
        print_error(f"Unknown variable: {variable}")

def print_settings():
    print("Current settings:")
    for key, value in global_settings.items():
        color = Fore.GREEN if value else Fore.RED
        print(f"{color}{key}: {value if value else 'Not set'}")

def show_instructions():
    print("""
Hello! Welcome to File Manager.
You can use the following commands:
1. set - Set the source, destination, or lists folder
   Usage: set <source_folder|destination_folder|lists_folder> <path>
   
2. copy_all - Copy all files from source folder to destination folder
   Usage: copy_all [source_folder] [destination_folder]
   If no folders are provided, it will use the globally set ones.
   
3. list_all - List all files in source folder and save to a JSON file in the destination folder
   Usage: list_all [source_folder] [destination_folder] [json_filename]
   If no folders are provided, it will use the globally set ones.
   
4. validate_all - Validate that all files in the source folder exist in the destination folder
   Usage: validate_all [source_folder] [destination_folder]
   If no folders are provided, it will use the globally set ones.

5. copy - Copy files from source to destination based on one or more JSON files
   Usage: copy <json_filename1> <json_filename2> ... validate
   The JSON files will be searched in the lists_folder, and the operation will use the globally set source and destination folders.
   The "validate" command at the end will validate all copied files.

6. validate - Validate that all files in the JSON list exist in the source folder
   Usage: validate <json_filename>
   The JSON file will be searched in the lists_folder, and the operation will use the globally set source folder.
   Also warns about files in the destination folder that are not in the JSON list.
   
7. settings - Print the current settings
   Usage: settings

8. menu - Print this menu again
   Usage: menu
""")

def execute_command(command):
    parts = command.strip().split()
    if len(parts) == 0:
        print_error("No command entered. Please try again.")
        return
    
    cmd = parts[0]
    
    if cmd == 'set' and len(parts) == 3:
        set_variable(parts[1], parts[2])
    elif cmd == 'copy_all':
        if len(parts) == 3:
            copy_all_files(parts[1], parts[2])
        else:
            copy_all_files()
    elif cmd == 'list_all':
        if len(parts) == 4:
            list_all_files_to_json(parts[1], parts[2], parts[3])
        else:
            list_all_files_to_json()
    elif cmd == 'validate_all':
        if len(parts) == 3:
            validate_all_files(parts[1], parts[2])
        else:
            validate_all_files()
    elif cmd == 'copy':
        if len(parts) >= 2:
            handle_copy_and_validate(parts)
        else:
            print_error("Usage: copy <json_filename1> <json_filename2> ... validate")
    elif cmd == 'validate':
        if len(parts) == 2:
            validate_list(parts[1])
        else:
            print_error("Usage: validate <json_filename>")
    elif cmd == 'settings':
        print_settings()
    elif cmd == 'menu':
        show_instructions()
    else:
        print_error("Invalid command or wrong number of arguments. Please try again.")

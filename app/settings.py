import json
import os

SETTINGS_FILE = 'settings.json'

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

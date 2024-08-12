import os
import readline
from settings import global_settings

# List of commands for auto-completion
commands = [
    "set",
    "copy",
    "list",
    "validate",
    "copy_list",
    "validate_list",
    "settings",
    "menu"
]

def complete_path(text, state):
    line = readline.get_line_buffer().split()
    
    if len(line) == 1:  # Command auto-completion
        matches = [cmd for cmd in commands if cmd.startswith(text)]
        if state < len(matches):
            return matches[state]
        else:
            return None
    elif line[0] in ["copy_list", "validate_list"]:
        # Auto-completion for file lists after "copy_list" or "validate_list"
        if global_settings['lists_folder']:
            lists_folder = global_settings['lists_folder']
            if os.path.isdir(lists_folder):
                options = [f for f in os.listdir(lists_folder) if f.startswith(text)]
                if state < len(options):
                    return options[state]
                else:
                    return None
    else:
        # General path auto-completion
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

def setup_completer():
    readline.set_completer(complete_path)
    readline.parse_and_bind("tab: complete")

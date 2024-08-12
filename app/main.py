from commands import execute_command, show_instructions
from settings import load_settings
import readline
from completer import setup_completer

def main():
    # Load settings at startup
    load_settings()

    # Setup tab completion for paths
    setup_completer()

    show_instructions()
    
    while True:
        command = input("> ")
        if command.lower() in ['exit', 'quit']:
            print("Exiting File Manager. Goodbye!")
            break
        execute_command(command)

if __name__ == '__main__':
    main()

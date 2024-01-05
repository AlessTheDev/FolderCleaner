from sys import argv
from sys import exit
import os

from CleanerSettings import CleanerSettings
from Utils import print_header

settings = CleanerSettings()

def main():
    if len(argv) == 1:
        # Get the current working directory
        dir_to_process = os.getcwd()
    elif len(argv) > 1:
        if argv[1].startswith("--"):
            handle_command(argv[1])
            return
        
        # Get specific directory
        dir_to_process = argv[1]
        if not os.path.exists(dir_to_process):
            print(f"Can't find directory: {dir_to_process}")
            exit(2)
    else:
        print("Invalid args")
        exit(1)
        
    process_dir(dir_to_process)

def handle_command(command):
    match command:
        case "--show-settings":
            settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
            os.startfile(settings_path)
        case "--settings":
            settings.load_settings(argv[2]) # argv[2] should be the settings file
            if len(argv) <= 3 or (len(argv) <= 4 and argv[3] == "-current"):  
                dir_to_process = os.getcwd()
            elif len(argv) <= 4:
                dir_to_process = argv[3]            
            if not os.path.exists(dir_to_process):
                print(f"Can't find directory: {dir_to_process}")
                exit(2)
            
            process_dir(dir_to_process)
        case "--group-all":
            if len(argv) <= 2 or (len(argv) <= 3 and argv[2] == "-current"):  
                dir_to_process = os.getcwd()
            elif len(argv) <= 3:
                dir_to_process = argv[2]            
            if not os.path.exists(dir_to_process):
                print(f"Can't find directory: {dir_to_process}")
                exit(2)
            group_dir(dir_to_process)
            
        case _: print("Invalid args")

def group_dir(path):
    """ Groups all the files in a directory based on their extension """
    try:
        files = os.listdir(path)
    except Exception:
        print("An error has occurred")
        exit(3)

    for file_name in files:
        print(f"Grouping... {file_name}")
        file_path = os.path.join(path, file_name)
        
        if os.path.isfile(file_path):
            group_file(file_name, path, os.path.splitext(file_name)[1].replace(".", ""))
            
    
        
def process_dir(path):
    """ Process all files in a directory """
    
    print_header(f"Processing {path}")
    
    try:
        files = os.listdir(path)
    except Exception:
        print("An error has occurred")
        exit(3)
    
    for file_name in files:
        file_path = os.path.join(path, file_name)
        
        if os.path.isfile(file_path):
            process_file(file_name, path)
            
def process_file(file_name, dir_path):
    """ Checks the settings and process a file based on the action """
    print(f"Processing {file_name}")
    
    actions = settings.get_file_actions()
    
    for act in actions:
        # Check if the file respects the settings
        if act["start"] != None:
            if not file_name.startswith(act["start"]):
                continue
        if act["end"] != None:
            if not file_name.endswith(act["end"]):
                continue
        
        # Execute file action
        match act["action"]:
            case "group": 
                # Create folder name
                start = "" if act["start"] is None else act["start"]
                end = "" if act["end"] is None else act["end"]
                group_name = start + end
                group_name.replace(".", "")
                
                group_file(file_name, dir_path, group_name)
            case "delete":
                os.remove(os.path.join(dir_path, file_name))
            case _: print("Invalid action")
            
def group_file(file_name, dir_path, group_name):
    """ Moves the file to a new folder based on the settings 'start' and 'end' fields """
    new_dir_name = settings.get_group_dirs_prefix() + group_name
    new_dir = os.path.join(dir_path, new_dir_name)
    
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    
    # Move the file
    os.rename(os.path.join(dir_path, file_name), os.path.join(new_dir, file_name))
        
main()
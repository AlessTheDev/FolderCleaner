from ast import Dict
from os import path
import json

class CleanerSettings:
    def __init__(self):
        
        with open(path.join(path.dirname(__file__), "settings.json"), 'r') as file:
            self.data = json.load(file)
    
    def load_settings(self, file):
        with open(file, 'r') as file:
            self.data = json.load(file)
    
    def get_file_actions(self) -> Dict:
        return self.data["file_actions"]
    
    def get_group_dirs_prefix(self):
        return self.data["group_dirs_prefix"]
    

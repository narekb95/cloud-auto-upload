import os
import json

import helpers

_config_file_name = 'config.json'
_config_file = os.path.join(helpers.App_Data, _config_file_name)

def create_config_file(target_folder):
    config_data = {
        "target": target_folder,
        "registry": []
    }
    print(f"Creating config file at {_config_file}")
    os.makedirs(helpers.App_Data, exist_ok=True)
    with open(_config_file, 'w') as f:
        json.dump(config_data, f)
        
class Config:
    def __init__(self):
        config = self.read_config()
        self.target_dir = config['target']
        self.files = config['registry']
        self.last_check = config['last-check'] if 'last-check' in config else 0

    def read_config(self):
        with open(_config_file, 'r') as f:
            return json.load(f)

    def update_config(self):
        with open(_config_file, 'w') as f:
            json.dump({
                'target': self.target_dir,
                'registry': self.files,
                'last-check': self.last_check
            }, f)

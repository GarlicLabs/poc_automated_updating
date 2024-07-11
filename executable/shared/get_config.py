import yaml
import sys

def get_config(config_file_path: str) -> dict:
    with open(config_file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
        return config
import yaml
import sys

def get_configAA() -> dict:
    path = sys.argv[1]
    with open(path, 'r') as config_file:
        config = yaml.safe_load(config_file)
        return config
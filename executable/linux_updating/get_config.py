import yaml

def get_config(path: str) -> dict:
    with open(path, 'r') as config_file:
        config = yaml.safe_load(config_file)
        return config
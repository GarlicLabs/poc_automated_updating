import git  # pip install gitpython

def pull(config: dict):
    git.Git(config["working_directory"]).clone(config["git_repo"])

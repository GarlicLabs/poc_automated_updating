import git
import urllib.parse

def clone(repository: dict):
    """
    config dict should look like:
    {
        "working_directory": "/tmp/working",
        "git_url": "git.example.com/repository.git",
        "git_username": "username",
        "git_password": "password"
    }
    Clones repo from given repository inside the working directory
    """
    git_url = repository["git_url"]
    git_username = urllib.parse.quote(repository["git_username"])
    git_password = urllib.parse.quote(repository["git_password"])

    clone_url = f"https://{git_username}:{git_password}@{git_url}"
    try:
        git.Git(repository["working_directory"]).clone(clone_url)
    except git.exc.GitCommandError as e:
        if e.stderr == "fatal: destination path 'repository' already exists and is not an empty directory.\n":
            pass
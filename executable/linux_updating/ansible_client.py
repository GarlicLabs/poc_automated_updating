import git
import subprocess
import os

def playbook(config: dict):
    git.Repo(config["directory"]).git.checkout(config["git_branch"])
    os.chdir(config["directory"])
    for playbook in config["playbooks"]:
        cmd = config["command"] + " " + playbook
        process = subprocess.Popen(cmd, shell=True)
        process.wait()

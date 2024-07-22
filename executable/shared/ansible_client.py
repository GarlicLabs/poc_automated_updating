import git
import subprocess
import os

def playbook(ansible_cmd: str, ansible_dir: str, branch: str, playbook: str):
    git.Repo(ansible_dir).git.checkout(branch)
    os.chdir(ansible_dir)
    cmd = ansible_cmd + " " + playbook
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.wait()

import subprocess
import os

def run_test(test_cmd: str, test_path: str, test_dir: str):
    os.chdir(test_dir)
    cmd = test_cmd + " " + test_path
    process = subprocess.Popen(cmd, shell=True)
    process.wait()
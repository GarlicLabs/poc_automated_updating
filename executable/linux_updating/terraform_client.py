import json 
import subprocess
import os

def apply(tf_dir: str, tf_options: str):
    tf_cmd = f"terraform apply {tf_options}"
    os.chdir(tf_dir)
    process = subprocess.Popen(tf_cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()

def destroy(tf_dir: str):
    tf_cmd = f"terraform destroy {tf_options}"
    os.chdir(tf_dir)
    process = subprocess.Popen(tf_cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()

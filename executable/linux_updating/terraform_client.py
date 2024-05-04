import subprocess
import os
import time

def apply(tf_dir: str, tf_options: str):
    tf_cmd = f"terraform apply {tf_options}"
    os.chdir(tf_dir)
    process = subprocess.Popen(tf_cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()
    # Sleep for 5min to wait for cloud-init 
    time.sleep(300)

def destroy(tf_dir: str, tf_options: str):
    tf_cmd = f"terraform destroy {tf_options}"
    os.chdir(tf_dir)
    process = subprocess.Popen(tf_cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()

from paramiko import SSHClient
import logging as log

def get_processes(server: dict):
    log.info(f"Get running processes from {server['host']}")
    client = SSHClient()
    try:
        client.load_system_host_keys()
        client.connect(hostname=server["host"], port=server["port"], username=server["user"])

        cmd = "systemctl list-units --type=service --state=running --no-legend | awk '{print $1}'"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        validate_stderr(stderr, server["host"])
        processes = stdout.read().decode().strip().split('\n')
        validate_stdout(processes, server["host"])

        return processes
    finally:
        client.close()

def validate_stderr(stderr, hostname: str):
    if stderr.read().decode():
        log.error("Error while getting processes from " + hostname)
        raise Exception(stderr.read().decode())

def validate_stdout(processes: list, hostname: str):
    if not processes:
        log.error("No processes found on " + hostname)
        raise Exception("No processes found on " + hostname)

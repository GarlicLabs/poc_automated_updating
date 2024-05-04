import terraform_client as tf
import ansible_client as ansible
import get_processes
from get_config import get_config
import os
import logging as log

log.basicConfig(level=log.DEBUG)

def main():
    log.info("Read config")
    config = get_config()

    log.info("Create temp working directory")
    create_working_directory(config["working_directory"])

    log.info("Provision test enviroment")
    # create_tf_test_env(config)
    # provision_test_env(config)

    log.info("Compare running processes prod <> test")
    compare_test_prod_running_processes(config)

    log.info("Check for open alerts")
    log.info("Upgrade!... do together")

def create_tf_test_env(config: dict):
    log.debug("Execute Terraform")
    tf.apply(config["test_env"]["terraform"]["directory"], config["test_env"]["terraform"]["options"])

def destroy_tf_test_env(config: dict):
    log.debug("Execute Terraform")
    tf.apply(config["test_env"]["terraform"]["directory"], config["test_env"]["terraform"]["options"])

def create_working_directory(dir: str):
    if not os.path.exists(dir):
        os.makedirs(dir)

def provision_test_env(config: dict):
    log.debug("Execute Ansible")
    ansible.playbook(config["test_env"]["ansible"])

def compare_test_prod_running_processes(config: dict):
    for server in config["servers"]:
        get_processes(server)

    # get running processes
    # login to test server
    # get running processes (save them somewhere)
    # compare prod and test processes

    log.debug("Get running processes prod")
    log.debug("Get running processes test")
    log.info("Show process diff")

    log.debug("Compare processes")
    ansible.playbook(config["compare_processes"]["ansible"])

if __name__ == "__main__":
    main()
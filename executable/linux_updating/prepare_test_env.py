import terraform_client as tf
import ansible_client as ansible
from get_processes import get_processes
import os
import logging as log


def prepare(config: dict):
    # obsolete
    #log.info("Create temp working directory")
    #create_working_directory(config["working_directory"])

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

    prod_process_server_dict = {}
    log.debug("Get running processes for prod")
    for server in config["prod_env"]["servers"]:
        processes = get_processes(server)
        prod_process_server_dict[server["tag"]] = processes

    test_process_server_dict = {}
    log.debug("Get running processes for test")
    for server in config["test_env"]["servers"]:
        processes = get_processes(server)
        test_process_server_dict[server["tag"]] = processes

    log.debug("Compare processes")
    for server in config["prod_env"]["servers"]:
        prod = prod_process_server_dict[server["tag"]]
        test = test_process_server_dict[server["tag"]]
        if test is None:
            continue

        diff = list(set(prod) - set(test))
        if diff != None:
            print(
                "There are differences between the hosts with the tag " + 
                server["tag"])
            print(diff)
            decision = input("Are these differences acceptable? (y/N): ")
            if decision == "y":
                pass
            else:
                raise Exception("Different Processes are not acceptable.")



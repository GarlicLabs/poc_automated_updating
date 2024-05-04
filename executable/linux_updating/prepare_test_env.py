import terraform_client as tf
import ansible_client as ansible
import get_processes
import os
import logging as log


def prepare(config: dict):
    log.info("Provision test enviroment")
    create_tf_test_env(config)
    provision_test_env(config)
    exit(0)

    log.info("Compare running processes prod <> test")
    compare_test_prod_running_processes(config)

    log.info("Check for open alerts")

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
    for playbook in config["test_env"]["ansible"]["playbooks"]:
        ansible.playbook(
        config["test_env"]["ansible"]["command"], 
        config["test_env"]["ansible"]["directory"], 
        config["test_env"]["ansible"]["git_branch"], 
        playbook)

def compare_test_prod_running_processes(config: dict):
    log.debug("Get running processes for prod")
    prod_process_server_dict = get_processes.get_mapped_processes(config["prod_env"]["servers"])
    
    log.debug("Get running processes for test")
    test_process_server_dict = get_processes.get_mapped_processes(config["test_env"]["servers"])
    
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



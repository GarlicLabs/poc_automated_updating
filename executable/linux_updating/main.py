import terraform_client as tf
import ansible_client as ansible
from get_processes import get_processes
from get_config import get_config
import os
import logging as log

# log.basicConfig(level=log.INFO)

def main():
    log.info("Read config")
    config = get_config()

    log.info("Create temp working directory")
    create_working_directory(config["working_directory"])

    log.info("Provision test enviroment")
    # create_tf_test_env(config)
    provision_test_env(config)

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
    for server in config["prod_env"]["servers"]:
        processes = get_processes(server)
        test_process_server_dict[server["tag"]] = processes

    log.debug("Compare processes")
    for server in config["prod_env"]["servers"]:
        prod = prod_process_server_dict[server["tag"]]
        print("=====================================")
        print(prod_process_server_dict[server["tag"]])
        test = test_process_server_dict[server["tag"]]
        print("=====================================")
        print(test_process_server_dict[server["tag"]])
        if test is None:
            continue

        diff = list(set(prod) - set(test))
        print(diff)
        if not diff:
            print(f"Server {server['tag']} is the same")
        

    # print(type(prod_tprocess_server_dict["control-plane01"])) 
    # print(test_process_server_dict)
    # for server in config["test_env"]["servers"]:
    #     prod = prod_process_server_dict[server["tag"]]
    #     test = tes_process_server_dict[server["tag"]]
    #     prod.sort()
    #     test.sort()
    #     print(prod) 

    # print(test_process_server_dict)


    # get running processes
    # login to test server
    # get running processes (save them somewhere)
    # compare prod and test processes

    log.debug("Get running processes prod")
    log.debug("Get running processes test")
    log.info("Show process diff")

    log.debug("Compare processes")
    # ansible.playbook(config["compare_processes"]["ansible"])

if __name__ == "__main__":
    main()
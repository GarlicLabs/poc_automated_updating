from shared import prepare_test_env
from shared import get_config
import logging as log
from shared import ansible_client as ansible
from shared import get_processes

log.basicConfig(level=log.INFO)

def main():
    log.info("Start linux update workflow with getting config")
    config = get_config.get_config()
    prepare_test_env.prepare(config)

    log.debug("Getting the running processes before update")
    test_pre_update_processes = get_processes.get_mapped_processes(
        config["test_env"]["servers"])

    log.info("Update test hosts via ansible")
    ansible.playbook(
        config["test_env"]["ansible"]["command"], 
        config["test_env"]["ansible"]["directory"], 
        config["test_env"]["ansible"]["git_branch"], 
        "playbooks/linux/update.yml")
    
    log.debug("Getting the running processes after update")
    test_post_update_processes = get_processes.get_mapped_processes(
        config["test_env"]["servers"])
    
    log.info("Compare running processes before and after update")
    for server in config["test_env"]["servers"]:
        pre = test_pre_update_processes[server["tag"]]
        post = test_post_update_processes[server["tag"]]
        if post is None:
            continue

        diff = list(set(pre) - set(post))
        if diff != None:
            print(
                "There are differences between the hosts with the tag " + 
                server["tag"])

    log.debug("Getting the running processes before prod update")
    prod_pre_update_processes = get_processes.get_mapped_processes(
        config["prod_env"]["servers"])

    log.info("Update prod hosts via ansible")
    ansible.playbook(
        config["prod_env"]["ansible"]["command"], 
        config["prod_env"]["ansible"]["directory"], 
        config["prod_env"]["ansible"]["git_branch"], 
        "playbooks/linux/update.yml")

    log.debug("Getting the running processes after prod update")
    prod_post_update_processes = get_processes.get_mapped_processes(
        config["prod_env"]["servers"])

    log.info("Compare running processes before and after prod update")
    for server in config["prod_env"]["servers"]:
        pre = prod_pre_update_processes[server["tag"]]
        post = prod_post_update_processes[server["tag"]]
        if post is None:
            continue

        diff = list(set(pre) - set(post))
        if diff != None:
            print(
                "There are differences between the hosts with the tag " + 
                server["tag"])


if __name__ == "__main__":
    main()
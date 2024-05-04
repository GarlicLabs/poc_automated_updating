from get_config import get_config
import prepare_test_env
import logging as log
import ansible_client
import get_processes

# log.basicConfig(level=log.INFO)

def main():
    log.info("Read config")
    config = get_config()
    prepare_test_env.prepare(config)
    log.info("Getting the running processes before update")
    pre_update_processes = get_processes.get_mapped_processes(
        config["test_env"]["servers"])   
    log.info("Update test hosts via ansible")
    ansible_client.playbook(
        config["test_env"]["ansible"]["command"], 
        config["test_env"]["ansible"]["directory"], 
        config["test_env"]["ansible"]["git_branch"], 
        "playbooks/linux/update.yml")
    log.info("Getting the running processes after update")
    post_update_processes = get_processes.get_mapped_processes(
        config["test_env"]["servers"])



if __name__ == "__main__":
    main()
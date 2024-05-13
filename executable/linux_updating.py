from shared import prepare_test_env
from shared import get_config
import logging as log
from shared import ansible_client as ansible
from shared import get_processes

# log.basicConfig(level=log.INFO)

def main():
    log.info("Read config")
    config = get_config.get_configAA()
    prepare_test_env.prepare(config)
    
    log.info("Getting the running processes before update")
    pre_update_processes = get_processes.get_mapped_processes(
        config["test_env"]["servers"])

    log.info("Update test hosts via ansible")
    #TODO Run one host after another, also add require input of user to continue
    ansible.playbook(
        config["test_env"]["ansible"]["command"], 
        config["test_env"]["ansible"]["directory"], 
        config["test_env"]["ansible"]["git_branch"], 
        "playbooks/linux/update.yml")
    
    log.info("Getting the running processes after update")
    post_update_processes = get_processes.get_mapped_processes(
        config["test_env"]["servers"])
    
    #TODO compare processes of test env pre and post
    #TODO compare processes of test post and prod
    #TODO trigger update prod env (save running processes, check for alerts, snapshot, run playbook, check procesess before and after)

if __name__ == "__main__":
    main()
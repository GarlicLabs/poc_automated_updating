from shared import prepare_test_env
from shared import get_config
import logging as log
from shared import ansible_client as ansible
from shared import get_processes
from executable.shared import test_client as testing
from shared import parse_flags

log.basicConfig(level=log.INFO)

def main():
    log.info("Start linux update workflow with getting config")
    flags = parse_flags.get_flags()
    config = get_config.get_config(flags.configFile)

    if flags.create_test_env:
        prepare_test_env.prepare(config)

    log.debug("Getting the running processes before update")
    test_pre_update_processes = get_processes.get_mapped_processes(
        config["test_env"]["servers"])

    log.info("Run tests before update on test")
    for test in config["robot_tests"]["tests"]:
        testing.run_test(config["robot_tests"]["command"], test,
                       config["robot_tests"]["directory"])

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
        if diff:
            print(
                "There are differences between the hosts with the tag " +
                server["tag"])

    log.info("Run tests after update on test")
    for test in config["robot_tests"]["tests"]:
        testing.run_test(config["robot_tests"]["command"], test,
                       config["robot_tests"]["directory"])

    if flags.update_prod:
        update_prod(config)

    if flags.destroy_test:
        log.info("Destroy test enviroment")
        prepare_test_env.destroy_tf_test_env(config)

def update_prod(config):
    log.debug("Getting the running processes before prod update")
    prod_pre_update_processes = get_processes.get_mapped_processes(config["prod_env"]["servers"])

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

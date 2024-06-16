import logging as log
from shared import get_config
from shared import prepare_test_env
from shared import ansible_client as ansible
from shared import robot_client as robot

log.basicConfig(level=log.INFO)


def main():
    log.info("Start kubernetes update workflow with getting config")
    config = get_config.get_config()
    log.info("Install and Configure test-environment")
    prepare_test_env.prepare(config)
    log.info("Run tests")
    for test in config["robot_tests"]["tests"]:
        robot.run_test(config["robot_tests"]["command"], test, 
                       config["robot_tests"]["directory"])
    log.info("All tests passed")
    
    log.info("Update test hosts via ansible")
    ansible.playbook(
        config["test_env"]["ansible"]["command"], 
        config["test_env"]["ansible"]["directory"], 
        config["test_env"]["ansible"]["git_branch"], 
        "playbooks/k8s/k8s_upgrade.yml")
    
    log.info("Run tests again after update on test")
    for test in config["robot_tests"]["tests"]:
        robot.run_test(config["robot_tests"]["command"], test, 
                       config["robot_tests"]["directory"])
    log.info("All tests passed")
    
    log.info("Update prod hosts via ansible")
    ansible.playbook(
        config["prod_env"]["ansible"]["command"], 
        config["prod_env"]["ansible"]["directory"], 
        config["prod_env"]["ansible"]["git_branch"], 
        "playbooks/k8s/k8s_upgrade.yml")
    
    log.info("Run tests again after update on prod")
    for test in config["robot_tests"]["tests"]:
        robot.run_test(config["robot_tests"]["command"], test, 
                       config["robot_tests"]["directory"])
    log.info("All tests passed")


if __name__ == "__main__":
    main()
from shared import prepare_test_env
from shared import get_config
import logging as log
from shared import ansible_client as ansible
from shared import get_processes
from shared import robot_client as robot
from shared import parse_flags

log.basicConfig(level=log.INFO)

def main():
    log.info("Start linux update workflow with getting config")
    flags = parse_flags.get_flags()
    config = get_config.get_config(flags.configFile)

    if flags.create_test_env:
        prepare_test_env.prepare(config)

    log.info("Run tests before update on test")
    for test in config["robot_tests"]["tests"]:
        robot.run_test(config["robot_tests"]["command"], test,
                       config["robot_tests"]["directory"])

    log.info("Update grafana via ansible")
    ansible.playbook(
        config["test_env"]["ansible"]["command"],
        config["test_env"]["ansible"]["directory"],
        "feature/grafana-update",
        "playbooks/k8s/SaaS/grafana.yml")

    log.info("Run tests after update on test")
    for test in config["robot_tests"]["tests"]:
        robot.run_test(config["robot_tests"]["command"], test,
                       config["robot_tests"]["directory"])

    if flags.update_prod:
        update_prod(config)

    if flags.destroy_test:
        log.info("Destroy test enviroment")
        prepare_test_env.destroy_tf_test_env(config)

def update_prod(config):

    log.info("Run tests before updating grafana on prod")
    for test in config["robot_tests"]["tests"]:
        robot.run_test(config["robot_tests"]["command"], test,
                       config["robot_tests"]["directory"])

    log.info("Update prod hosts via ansible")
    ansible.playbook(
        config["prod_env"]["ansible"]["command"],
        config["prod_env"]["ansible"]["directory"],
        config["prod_env"]["ansible"]["git_branch"],
        "playbooks/k8s/SaaS/grafana.yml")

    log.info("Run tests after updating grafana on prod")
    for test in config["robot_tests"]["tests"]:
        robot.run_test(config["robot_tests"]["command"], test,
                       config["robot_tests"]["directory"])

if __name__ == "__main__":
    main()

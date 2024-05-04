import terraform_client as tf
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
    create_tf_test_env(config)

    log.debug("Execute Ansible")
    log.info("Compare running processes prod <> test")
    log.debug("Get running processes prod")
    log.debug("Get running processes test")
    log.info("Show process diff")
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

if __name__ == "__main__":
    main()
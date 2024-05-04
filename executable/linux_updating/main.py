import git_client as git
from get_config import get_config
import os
import logging as log

def main():
    log.info("Read config")
    config = get_config()

    log.info("Create temp working directory")
    create_working_directory(config["working_directory"])

    log.info("Provision test enviroment")
    execute_terraform(config)

    log.debug("Execute Ansible")
    log.info("Compare running processes prod <> test")
    log.debug("Get running processes prod")
    log.debug("Get running processes test")
    log.info("Show process diff")
    log.info("Check for open alerts")
    log.info("Upgrade!... do together")

def execute_terraform(config: dict):
    log.debug("Clone Terraform repository")
    clone_config = dict(
        working_directory=config["working_directory"],
        git_url=config["terraform"]["git_url"],
        git_username=config["terraform"]["username"],
        git_password=config["terraform"]["password"]
    )
    git.clone(clone_config)
    log.debug("Execute Terraform")

def create_working_directory(dir: str):
    if not os.path.exists(dir):
        os.makedirs(dir)

if __name__ == "__main__":
    main()
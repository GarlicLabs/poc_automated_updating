import git_clone as git_clone
import logging as log
import os

def main():
    log.info("Read config")
    log.info("Create temp working directory")
    create_working_directory("/tmp/linux_updating/")

    log.info("Provision test enviroment")
    execute_terraform(None)

    log.debug("Execute Ansible")
    log.info("Compare running processes prod <> test")
    log.debug("Get running processes prod")
    log.debug("Get running processes test")
    log.info("Show process diff")
    log.info("Check for open alerts")
    log.info("Upgrade!... do together")

def execute_terraform(config: dict):
    git_clone.pull(config)
    log.debug("Execute Terraform")

def create_working_directory(dir: str):
    if not os.path.exists(dir):
        os.makedirs(dir)

if __name__ == "__main__":
    main()
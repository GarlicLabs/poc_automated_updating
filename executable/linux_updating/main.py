from get_config import get_config
import logging as log
import sys

def main():
    log.info("Read config")
    config_file = sys.argv[1]
    config = get_config(config_file)
    print(config)
    log.info("Provision test enviroment")
    log.debug("Execute Terraform")
    log.debug("Execute Ansible")
    log.info("Compare running processes prod <> test")
    log.debug("Get running processes prod")
    log.debug("Get running processes test")
    log.info("Show process diff")
    log.info("Check for open alerts")
    log.info("Upgrade!... do together")

if __name__ == "__main__":
    main()
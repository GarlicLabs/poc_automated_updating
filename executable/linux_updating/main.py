from get_config import get_config
import prepare_test_env
import logging as log

# log.basicConfig(level=log.INFO)

def main():
    log.info("Read config")
    config = get_config()
    prepare_test_env.prepare(config)

if __name__ == "__main__":
    main()
import argparse

def get_flags():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('configFile')
    parser.add_argument('--create-test-env',
                    action='store_true')
    parser.add_argument('--update-prod',
                    action='store_true')
    parser.add_argument('--destroy-test',
                    action='store_true')
    return parser.parse_args()

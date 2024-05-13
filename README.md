# POC automated updates

## Setup

1. Create venv `python3 -m venv ./venv`
2. Install dependencies `venv/bin/pip install -r requirements.txt`

## Update dependency file

`venv/bin/pip3 freeze > requirements.txt`

## Execute

`venv/bin/python3 executable/linux_updating/main.py executable/linux_updating/config.yml`

## Flow

Need 3 files:

Updating Linux

There are two modes(prod & test mode) (for poc reasons just implement the test mode)
- prod mode will have more features like backup/rollback...

- Create tmp test env
- Use existing ansible roles to provision env
Now the state of the tmp test env, should be the same as the prod env 
- Get running systemd services from prod and test env and compare?
- Anyways definitly get running systemd services from test env
- Check health of tmp test env with prometheus alertmanager
- Execute upgrade (Where does this code lays? is it in infra_config? an own branch?)
- Execute dist upgrade
- Get running systemd services and compare with list before update, if it does not match, show the difference

Updating k8s

- Create tmp test env
- Use existing ansible roles to provision env
- Deploy all software 
- Get list of running pods from prod and compare with test env
- Upgrade k8s
...

Updating grafana

-----

executable/linux_updating.py
executable/k8s_updating.py
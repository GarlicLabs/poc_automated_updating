
# - Create tmp test env
# - Use existing ansible roles to provision env
# Now the state of the tmp test env, should be the same as the prod env 
# - Get running systemd services from prod and test env and compare?
# - Anyways definitly get running systemd services from test env
# - Check health of tmp test env with prometheus alertmanager
# - Execute upgrade (Where does this code lays? is it in infra_config? an own branch?)
# - Execute dist upgrade
# - Get running systemd services and compare with list before update, if it does not match, show the difference


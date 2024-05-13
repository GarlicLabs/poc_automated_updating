# 1 Prepare test env
# 1.1 Provision and configure test vms
# 2. Execute k8s_setup playbook with current prod version
# 3. Run robot tests
# 4. Check for alerts
# 5. Do snapshosts
# 6. Trigger update playbook
# 7. Run robot tests against new version
# 8. Do same for prod

# Prod playbooks common.yml, k8s_setup.yml, playbooks/k8s/SaaS/grafana.yml
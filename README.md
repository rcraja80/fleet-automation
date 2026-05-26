# Filesystem Usage Monitor

Local test setup for checking filesystem usage over 80% using Python + Ansible.

## Files
- inventory/hosts.ini
- scripts/fs_check.py
- playbooks/run_fs_check.yml
- Jenkinsfile

## Run locally
```bash
ansible-playbook -i inventory/hosts.ini playbooks/run_fs_check.yml
```

## Expected behavior
- Exit code 0: no filesystem above threshold
- Exit code 2: one or more filesystems above threshold

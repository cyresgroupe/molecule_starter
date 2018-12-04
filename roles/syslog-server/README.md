install/syslog-server
==============

This role install a simple rsyslog server

The Rsyslog server put log files into /var/log/HOSTS/{{hostname}}

Requirements
------------

- This is a role for RHEL server only

Role Variables
--------------

- none

Dependencies
------------

No dependencies

Example Playbook
----------------

Exemple 1:

```yaml
- hosts: servers
  become: yes
  roles:
    - install/syslog-server
```

License
-------

BSD

Author Information
------------------

Cyres made.

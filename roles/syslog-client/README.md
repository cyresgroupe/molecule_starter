install/syslog-client
==============

This role install a simple rsyslog client to connect to a server

Requirements
------------

- This is a role for RHEL server only

Role Variables
--------------

- rsyslog_server (string)

Example Playbook
----------------

Exemple 1:

```yaml
- hosts: servers
  become: yes
  rsyslog_server: rsyslog.mycompany.net
  roles:
    - install/syslog-server
```

Molecule build
-------
Two scenario exists
- **default** : for unit testing and code coverage
- **syslog-interco** : that build a server and a client to test interco between them

License
-------

BSD

Author Information
------------------

Cyres made.

# molecule_starter
Start with Ansible Molecule with this two Ansible Syslog roles

## I. Start with Molecule
Here is a Digital Ocean [article](https://www.digitalocean.com/community/tutorials/how-to-test-ansible-roles-with-molecule-on-ubuntu-16-04), very good to start with

## II. Installation
You can follow the steps in the article, or you can follow our. This repo works on RHEL server.
In order to make it work I needed to install : python-devel & gcc
- Install pip

```bash
$> sudo easy_install pip
```
Make sure to have easy_install. This is not the best way but it works for test and learning purpose.
- Install requirements

```bash
$> pip install -r requirements.txt
```

Now you can start playing with Molecule

## III. Testing default scenarios
### Syslog-client
```bash
$> cd roles
$> cd syslog-client
$> molecule test
[...]                   # This should works
```
The command *test* launch every step of the default scenario. At the end the role works fine against the tests we wrote :
```python
[...]

@pytest.mark.parametrize("name", [
    ("rsyslog")
])
def test_build_dependencies(host, name):
    pkg = host.package(name)
    assert pkg.is_installed


def test_rsyslog_file(host):
    f = host.file('/etc/rsyslog.conf')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_socket_listening_udp(host):
    result = host.run("sudo netstat -tulpn | grep rsyslog | grep udp | wc -l")

    assert result.rc == 0 and '1' in result.stdout
```

### Syslog-server
```bash
$> cd roles
$> cd syslog-server
$> molecule test
[...]                   # This should works
```
Here is the tests we wrote for testing the server :
```python
[...]

def test_build_dependencies(host):
    pkg = host.package("rsyslog")

    assert pkg.is_installed


def test_enabled_package(host):
    service = host.service("rsyslog")

    assert service.is_enabled
    assert service.is_running


def test_rsyslog_file(host):
    f = host.file('/etc/rsyslog.conf')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_rsyslog_file_contains_custom_values(host):
    conf = host.file('/etc/rsyslog.conf').content

    assert b'#$ModLoad imudp' not in conf
    assert b'#$UDPServerRun 514' not in conf
    assert b'#$ModLoad imtcp' not in conf
    assert b'#$InputTCPServerRun 514' not in conf
    assert b'$ModLoad imudp' in conf
    assert b'$UDPServerRun 514' in conf
    assert b'$ModLoad imtcp' in conf
    assert b'$InputTCPServerRun 514' in conf


def test_socket_listening_tcp(host):
    result = host.run("sudo netstat -tulpn | grep rsyslog | grep tcp | wc -l")

    assert result.rc == 0 and '2' in result.stdout


def test_socket_listening_udp(host):
    result = host.run("sudo netstat -tulpn | grep rsyslog | grep udp | wc -l")

    assert result.rc == 0 and '2' in result.stdout
```

## IV. Use a custom scenario
In order to validate the client against the server, we create another scenario in the role Syslog-server. The scenario build two instances and configure them accordingly to the molecule.yml we made. (You can add as many as you want in a moleculized role)

To init a scenario different from default :
```bash
$> cd roles/
$> cd syslog-server/
$> molecule init scenario --role-name syslog-server --scenario-name syslog-interco
```

### Molecule.yml
This is the way we configure two instance to test Client Server interactions
```yaml
---
dependency:
    name: galaxy
driver:
    name: docker
lint:
    name: yamllint
    options:
        config-data:
            rules:
                truthy: disable             # Custom properties to handle boolean best practices in Ansible
platforms:
  - name: instance-syslog-server
    image: milcom/centos7-systemd
    privileged: true
    groups:
        - server
  - name: instance-syslog-client
    image: milcom/centos7-systemd
    privileged: true
    groups:
        - client
provisioner:
    name: ansible
    lint:
      name: ansible-lint
    playbooks:
        prepare: prepare.yml               # Custom prepare playbook to handle testinfra requirements we don't want to have in the role
scenario:
    name: syslog-interco
verifier:
    name: testinfra
    lint:
      name: flake8
```
You can see two "platforms" item. One for the client, and one for the server. The group spec is important, we use it to call ansible play against.

### playbook.yml
```yaml
---
- name: Converge server
  hosts: server
  roles:
    - syslog-server

- name: Converge client
  hosts: client
  pre_tasks:
    - name: Get server IP
      command: hostname -I
      register: ip
      delegate_to: "{{groups['server'][0]}}"
      changed_when: no

    - name: Set facts
      set_fact:
          rsyslog_server: "{{ip.stdout}}"
      changed_when: no
  roles:
    - ../syslog-client
```

In the main playbook called by Molecule during the "prepare" phase, there are two plays.
- The first one initialize the Syslog server based on our role, it's called on the server group of instances.
- The second one call the client role on client instance group.

### Aditionnals tweak
#### Ansible booleans best practice
Ansible best practice ask to set booleans with "yes" or "no" string. The Yaml linter don't like it. To get rid of the warning (that failed the run), you can add this property to the linter, in molecule.yml:
```yaml
[...]
name: yamllint
options:
    config-data:
        rules:
            truthy: disable
[...]
```

#### Client internal IP
We set up a tweak to get the internal IP of the instance. Ansible facts don't bring it to us...
#### Testinfra preriquisites
We create a prepare playbook that is apply after the creation and before the converge step. This playbook install net-tools in order to let testinfra run some tests but without adding net-tools in the role itself. Very usefull...

### Test both roles
```bash
$> cd roles
$> cd syslog-server
$> molecule test -s syslog-interco
[...]                                   # This should works
```

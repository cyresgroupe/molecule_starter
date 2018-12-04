import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('server')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_hosts_dir_properties(host):
    dir = host.file('/var/log/HOSTS')

    assert dir.is_directory
    assert dir.user == 'root'
    assert dir.group == 'root'


def test_if_client_dir_exists(host):
    dir = host.file('/var/log/HOSTS/instance-syslog-client')

    assert dir.is_directory
    assert dir.user == 'root'
    assert dir.group == 'root'

import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


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

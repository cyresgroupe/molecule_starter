import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


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

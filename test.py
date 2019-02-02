# -*- coding:utf8 -*-

# system tests

def test_system_info(host):
    assert host.system_info.distribution == "centos"
    assert "7.6" in host.run("cat /etc/redhat-release").stdout

# webservers tests

def test_apache_is_installed(host):
    httpd = host.package("httpd")
    assert httpd.is_installed
    assert httpd.version.startswith("2.4")

def test_apache_running_and_enabled(host):
    httpd = host.service("httpd")
    assert httpd.is_running
    assert httpd.is_enabled

def test_apache_is_listening(host):
    assert host.socket("tcp://0.0.0.0:80").is_listening

def test_ruby_is_installed(host):
    assert host.exists("ruby")
    assert "2.5" in host.run("ruby -v").stdout

def test_rails_is_installed(host):
    assert host.exists("rails")
    assert "5.2.2" in host.run("rails -v").stdout

# dbservers tests

def test_postgresql_is_installed(host):
    postgresql = host.package("postgresql96")
    assert postgresql.is_installed
    assert postgresql.version.startswith("9.6")

def test_postgresql_running_and_enabled(host):
    postgresql = host.service("postgresql-9.6")
    assert postgresql.is_running
    assert postgresql.is_enabled

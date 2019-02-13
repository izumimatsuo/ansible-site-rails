# -*- coding:utf8 -*-

def test_apache_is_installed(host):
    httpd = host.package("httpd")
    assert httpd.is_installed
    assert httpd.version.startswith("2.4.6")

def test_apache_running_and_enabled(host):
    httpd = host.service("httpd")
    assert httpd.is_running
    assert httpd.is_enabled

def test_apache_is_listening(host):
    assert host.socket("tcp://0.0.0.0:80").is_listening

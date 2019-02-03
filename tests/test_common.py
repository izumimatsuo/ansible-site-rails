# -*- coding:utf8 -*-

# system tests

def test_system_info(host):
    assert host.system_info.distribution == "centos"
    assert "7.6" in host.run("cat /etc/redhat-release").stdout

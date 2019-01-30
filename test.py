# -*- coding:utf8 -*-

def test_apache_is_installed(host):
  httpd = host.package("httpd")
  assert httpd.is_installed


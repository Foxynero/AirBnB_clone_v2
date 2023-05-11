#!/usr/bin/python3
"""
Fabric script to distribute archived web_static files to web servers
"""
from fabric.api import local


def do_deploy(archive_path):
    """
    distributes archived web_static from do_pack() to web servers
    """
    if archive_path is None:
        return False
    return True

#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.

from fabric.api import *
import os.path

env.user = 'ubuntu'
env.hosts = ['54.146.76.82', '54.165.77.174']


def do_deploy(archive_path):
    """Fabric script that distrubutes an archive to server"""
    if os.path.exists(archive_path):
        new_path = archive_path.replace('versions/', '')
        file_name = new_path[:-4]
        arc_folder = "/data/web_static/releases/{}".format(new_path)
        put(archive_path, '/tmp/')
        run('mkdir -p /data/web_static/releases/{}'.format(file_name))
        run('tar -xzf /tmp/{} -C {}'.format(new_path, arc_folder[:-4]))
        run('rm /tmp/{}'.format(new_path))
        run('mv {}/web_static/* {}/'.format(arc_folder[:-4], arc_folder[:-4]))
        run('rm -rf {}/web_static'.format(arc_folder[:-4]))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(arc_folder[:-4]))
        return True
    else:
        return False

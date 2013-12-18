# -*- coding: utf-8 -*-
from fabric.context_managers import cd
from fabric.operations import local, run
from fabric.state import env

__author__ = 'patrickz'

env.hosts=['115.29.41.2']
env.user = 'root'
env.key_filename = '~/.ssh/id_rsa.pub'

def push():
    local('git add .; git commit; git push origin master')

def update():
    with cd('/opt/pkgs/king_crawl'):
        run('git pull')

def deploy():
    push()
    update()
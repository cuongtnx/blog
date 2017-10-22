from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from fabric.operations import prompt

from publishconf import *


####################
# CONFIGS
####################
# ENVIRONMENT setup
env.hosts = [SERVER_IP]
env.nginx_from = NGINX_FROM
env.nginx_to = NGINX_TO
env.project_dir = PROJECT_REMOTE_DIR
env.project_local_dir = PROJECT_LOCAL_DIR
env.project_url = PROJECT_URL
env.user = REMOTE_USER
env.virtualenv_remote = VIRTUALENV_REMOTE


####################
# TASKS
####################
def _secure_ssh():
    env.user = ROOT
    run('adduser %s' % REMOTE_USER)
    run('usermod -aG sudo %s' % REMOTE_USER)  # make sudo user
    # generate ssh key
    #   if already have a ssh_key
    #   and enable ssh in Digital Ocean, which means password ssh has
    #   already been disabled
    ssh_folder = '/home/%s/.ssh' % REMOTE_USER
    run('mkdir -p %s' % ssh_folder)
    sudo('chown %s %s' % (REMOTE_USER, ssh_folder))
    sudo('chmod 700 %s' % ssh_folder)
    put('~/.ssh/id_rsa_learn.pub', '%s/authorized_keys' % ssh_folder, mode=755)
    sudo('chown %s %s/authorized_keys' % (REMOTE_USER, ssh_folder))

    #   if doesn't have ssh_key
    #   if doesn't enable ssh in Digital Ocean
    #       just use ssh-copy-id REMOTE_USER@SERVER_PI
    #       disable password authentication
    # disable root login
    # run('sed -i 's:RootLogin yes:RootLogin no:' /etc/ssh/sshd_config')
    # run('service ssh restart')
    env.user = REMOTE_USER


def _install_packages():
    sudo('apt-get update')
    sudo('apt-get upgrade -y')
    sudo('apt-get install -y python3 python3-pip')
    sudo('apt-get install -y git-core nginx postgresql memcached supervisor')
    sudo('apt-get install -y\
            build-essential libssl-dev libffi-dev python3-dev')
    sudo('pip3 install -U pip')
    sudo('pip3 install -U virtualenv')


def _push_changes():
    local('git push origin master')


def _clone_project():
    if exists(env.project_dir):
        with cd(env.project_dir):
            run('git pull origin master')
    else:
        run('git clone %s' % env.project_url)


def _set_up_virtualenv():
    if (exists(env.virtualenv_remote) and
            confirm('Virtualenv already exists, would you like to replace it?')):
        run('rm -rf %s' % env.virtualenv_remote)
    else:
        run('virtualenv -p python3 %s' % env.virtualenv_remote)

    _virtualenv('pip install -r requirements.txt')


def _virtualenv(command):
    """
    Wrapper to run command inside the virtualenv environment
    """
    with cd(env.project_dir):
        with prefix('source %s/bin/activate' % env.virtualenv_remote):
            run(command)


def _run_project_tasks():
    _virtualenv('pelican -d -s publishconf.py')


def _update_nginx():
    sudo('cp %s %s' % (env.nginx_from, env.nginx_to))
    sudo('service nginx restart')


def _setup_nginx():
    sudo('rm /etc/nginx/sites-enabled/default')
    _update_nginx()


####################
# INTERFACES
####################
def setup():
    """
    Setup new VPS server
        1. Add new sudo user, enable ssh login and disable ssh-ing with root
        2. Install required packages to run a Python web server
    """
    # Currently, the first task is performed directly by SSH-ing into server
    # as root. But in the future, these should be automated.
    # _secure_ssh()
    _install_packages()


def create():
    _setup_nginx()


def deploy():
    """
    Deployment tasks
        1. Run local tasks
    """
    _push_changes()
    _clone_project()
    _set_up_virtualenv()
    _run_project_tasks()
    _update_nginx()


def new():
    """
    Create new file with header
    """
    from datetime import date
    file_date = str(date.today())
    file_title = prompt("What is your entry's title?")
    file_slug = "-".join(file_title.lower().split(" "))
    file_header = """Title: %s\nDate: %s\n""" % (file_title, file_date)

    with open("%s/%s-%s.md" % (PATH, file_date, file_slug), 'w') as f:
        f.write(file_header)
        f.close()

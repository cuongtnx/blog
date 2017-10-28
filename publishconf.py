import os
import sys

sys.path.append(os.curdir)

from pelicanconf import *

SITEURL = 'https://blog.cuongtn.xyz'
RELATIVE_URLS = False

LOCAL_USER = 'cuongtn'
REMOTE_USER = 'cuongtn'
ROOT = 'root'
SERVER_IP = '138.197.130.199'

PROJECT_LOCAL_DIR = '/home/%s/working/blog' % LOCAL_USER
PROJECT_REMOTE_DIR = '/home/%s/blog' % REMOTE_USER
PROJECT_URL = 'https://github.com/cuongtnx/blog.git'

VIRTUALENV_REMOTE = '/home/%s/blog/env' % REMOTE_USER

NGINX_FROM = '%s/deployment/blog.conf' % PROJECT_REMOTE_DIR
NGINX_TO = '/etc/nginx/conf.d/blog.conf'

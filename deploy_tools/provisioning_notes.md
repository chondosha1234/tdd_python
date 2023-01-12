Provisioning a new site
=======================

## Required Packages:

* nginx
* Python 3.*
* virtualenv + pip
* Git

e.g. on Ubuntu:

    sudo add-apt-repository ppa:deadsnakes/ppa (?)
    sudo apt update
    sudo apt install nginx git python3.7 python3.7-venv

## Nginx Virtual Hosting config

* see nginx.template.conf
* replace DOMAIN with, e.g. staging.my-domain.com

## Systemd service

* see gunicorn-systemd.template.service
* replace DOMAIN with, e.g. staging.my-domain.com

## folder structure:

Assume we have user account at home/username

/home/username
|___ sites
    |___ DOMAIN1
    |      |___ .env
    |      |___ db.sqlite3
    |      |___ manage.py etc
    |      |___ static
    |      |___ virtualenv
    |
    |___ DOMAIN2
          |___ .env
          |___ db.sqlite3
          |___ etc

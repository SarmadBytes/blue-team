# pfj-appsec-software-requests

The AppSec Service Catelog allows you to manage your workflows within a security program.
This application streamlines requests and allow them to be filter within the correct pipelines.


### Prerequisites
The following is a list of prerequisites that may need to be installed before Django will work
```
Python >= 3.7
pip Django >= 2.2.6
pip jira >= 2.0.0
Red Hat Linux Enterprise >= 8.0.1905
```

## Quick Start

```
git clone https://github.com/PilotFlyingJ/pfj-appsec-software-requests
cd pfj-appsec-software-requests
# running
python manage.py runserver
```

## Installation
The following guide will walk you through installation from a brand-new RHEL box perspective.
### Install Git and wget on RHEL with the following:
```
sudo yum install git
sudo yum install wget
```

### Create the "django" directory in /opt and cd to that new created directory:
```
sudo mkdir /opt/django/
cd /opt/django/
```

### Clone this directory using the following commands:
```
sudo git clone https://github.com/PilotFlyingJ/pfj-appsec-software-requests.git
Username for 'https://github.com':
Password for 'https://john.doe@github.com':
```

### Install Python3 and the pip requirements:
#### Python3
```
sudo yum update
sudo yum install centos-release-scl
sudo yum install gcc openssl-devel bzip2-devel
sudo wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
sudo tar xzf Python-3.7.2.tgz
cd Python-3.7.2.tgz
sudo ./configure ––enable–optimizations
sudo make altinstall
cd ..
sudo rm -r Python-3.7.2
sudo rm Python-3.7.2.tgz
```
#### Pip3
```
cd pfj-appsec-software-requests
sudo yum install python3-pip
sudo pip3 install -r requirments.txt
```
#### SQLite
depending on your build of RHEL you may have to manually update SQLite
```
wget https://kojipkgs.fedoraproject.org//packages/sqlite/3.8.11/1.fc21/x86_64/sqlite-devel-3.8.11-1.fc21.x86_64.rpm
wget https://kojipkgs.fedoraproject.org//packages/sqlite/3.8.11/1.fc21/x86_64/sqlite-3.8.11-1.fc21.x86_64.rpm
sudo yum install sqlite-3.8.11-1.fc21.x86_64.rpm sqlite-devel-3.8.11-1.fc21.x86_64.rpm
```

### Apache
Now that we have the code for Django we need to install a web server to host our code, we will be using apache to accomplish this.
```
sudo yum install httpd
sudo yum install centos-release-scl
sudo yum install rh-python36 rh-python36-mod_wsgi
```

### Configure Apache
```
sudo mkdir /etc/httpd/sites-available /etc/httpd/sites-enabled
sudo mv /opt/django/pfj-appsec-software-requests/000-default.conf /etc/httpd/sites-available/000-default.conf
sudo mv /opt/django/pfj-appsec-software-requests/default-ssl.conf /etc/httpd/sites-available/default-ssl.conf
```

https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-14-04

https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-centos-7
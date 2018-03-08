#!/bin/bash
echo "Starting provision"
echo "Installing updates, upgrades, and enviroments"
apt-get install openssh-server
apt-get update && apt-get -y upgrade
apt-get -y install apache2 python-pip libapache2-mod-wsgi 
apt-get -y install  python-dev libpq-dev postgresql postgresql-contrib

 apt-get install debconf-utils
 export DEBIAN_FRONTEND=noninteractive
 apt-get -y install virtualenv --fix-missing
cd /opt/
virtualenv django-env
cd django-env
. bin/activate

su - postgres
echo 'database setup'

echo "CREATE DATABASE kkidb;
CREATE USER kkidb WITH PASSWORD 'catdb';
ALTER ROLE kkidb SET client_encoding TO 'utf8';
ALTER ROLE kkidb SET default_transaction_isolation TO 'read committed';
ALTER ROLE kkidb SET timezone to 'UTC';
GRANT ALL PRIVILEGES ON DATABASE kkidb TO kkidb;" | sudo -u postgres psql;


echo 'installing Django'
sudo python -m pip install --upgrade pip
sudo pip install django
sudo django-admin startproject kkidb
cat > /etc/apache2/conf-available/kkidb.conf <<EOF
WSGIScriptAlias / /opt/django-env/kkidb/kkidb/wsgi.py
WSGIPythonPath /opt/django-env/kkidb:/opt/django-env/lib/python2.7/site-packages

<Directory /opt/django-env/kkidb>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
EOF

sudo -y apt-get install python-psycopg2 --fix-missing
sudo pip install django psycopg2
sudo a2enconf kkidb
sudo systemctl restart apache2.service 

echo 'Establishing database.'
cd kkidb
sudo python manage.py startapp catdb
cd ..
sudo cp -r /../../kkidb_static/* kkidb/


echo 'I HAVE BEEN SUMMONED!'
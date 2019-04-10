# IOT Web Platform
The web platform component for the IOT Intrusion Detection System.
## Members
joshuaspring9 is Joshua Zeitlinger  
vpilly is Varun Pilly  
jslavens99 is Jake Slavens  
kzambrow is Kamil Zambrowski
## Requirements
You will need a local installation of Python 3, pip3, and a [MySQL](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04) server to host the database.

Run the following commands to install Django and some of its dependencies:
```python
pip3 install Django
```
```python
pip3 install django-allauth pillow
```
## Prerequisites
Local, configuration-specific settings like database credentials should be placed in `iot-intrusion-detection/local_settings.py`, which is included in `settings.py` and not part of version control.  A default version is specified at `iot-intrusion-detection/local_settings_dist.py` which you can rename to `local_settings.py`.  After you have specified the database credentials, you will need to populate the database structure with:
```bash
mysql -u root -p <<EOF
DROP DATABASE IF EXISTS django_dashboard;
CREATE DATABASE django_dashboard;
EOF
```
```python
python3 manage.py migrate
```
or just run
```bash
bash reset.sh
```
## Running the development server
From the project's root directory:
```python
python3 manage.py runserver
```
## Updating models
Every time you update a model in `models.py`, you will need to update the database structure with:
```python
python3 manage.py makemigrations
```
followed by
```python
python3 manage.py migrate
```

## Resetting Database
To reset the user login database, run the following command:
```bash
bash reset.sh
```

This command is if you entered the wrong user or password into the bash reset command:
```bash
bash setup.sh
```

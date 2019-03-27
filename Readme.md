# IOT Web Platform
The web platform component for the IOT Intrusion Detection System.
## Requirements
Run the following command to install dependencies:
```python
pip install django-allauth pillow
```
You will also need a local installation of a MySQL server to host the database. 
## Prerequisites
Local, configuration-specific settings like database credentials should be placed in `iot-intrusion-detection/local_settings.py`, which is included in `settings.py` and not part of version control.  A default version is specified at `iot-intrusion-detection/local_settings_dist.py` which you can rename to `local-settings.py`.  After you have specified the database credentials, you will need to populate the database structure with:
```python
python3 manage.py migrate
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
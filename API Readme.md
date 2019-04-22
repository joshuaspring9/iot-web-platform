# API
The iot-web-platform is equipped with a fully functional, RESTful API that currently supports interacting with Users, Datafiles, and Smart Home Devices.
## Permissions
In order to access the API, you must have admin permissions, or be granted model-specific permissions to interact with a particular model.  You can give admin permissions to a user through the [admin interface](http://localhost:8000/admin/).
## Accessing
In your web browser, you may navigate to <http://localhost:8000/api/> which will expose a nice interface to explore the API functionality.
## Authentication
### Session based
When you visit the API in your web browser, you are authenticated through Django's session-based authentication which you also use to sign in to the web platform.
### OAuth2 based
You can also authenticate by using OAuth 2, which will give you an access token that you can use in any number of applications or scripts.  To obtain an OAuth 2 token, you must follow the following process:
#### Initial setup: Create an app
1. Navigate to <http://localhost:8000/o/applications/>
2. Create a new application and fill the form with the following data:
    - Name: just a name of your choice
    - Client Type: confidential
    - Authorization Grant Type: Resource owner password-based

This will give you a `client_id` and `client_secret` which you will need when obtaining an authentication token for a user.
#### Exchanging a username and password for an authentication token
Run the following command, replacing `<username>`, `<password>`, `<client_id>`, and `<client_secret>` with your actual credentials:
```bash
curl -X POST -d "grant_type=password&username=<user_name>&password=<password>" -u"<client_id>:<client_secret>" http://localhost:8000/api/o/token/
```

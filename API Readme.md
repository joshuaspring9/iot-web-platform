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
You can also authenticate by using OAuth 2, which will give you an access token that you can use in any number of applications or scripts.
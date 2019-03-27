EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = 'gmail account'
EMAIL_HOST_PASSWORD = 'gmail password'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_dashboard',
        'USER': 'django',
        'PASSWORD': 'Ilikepython',
        'HOST': 'localhost',
    }
}

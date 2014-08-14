"""
Django settings for humor project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9eg&%!9_!vbp6p)()!#mh&+-^ludf1gj^_*e^*y(8-a7-^snaw'


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), '../templates')
)




# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'thirdpart',
    'joke',
    'imgs'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
)

ROOT_URLCONF = 'humor.urls'

WSGI_APPLICATION = 'humor.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

if 'SERVER_SOFTWARE' in os.environ:
    from sae.const import (
     MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
    )

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False
    TEMPLATE_DEBUG = False
    ALLOWED_HOSTS = ['humors.sinaapp.com']
else:
    MYSQL_HOST = ''
    MYSQL_PORT = '3307'
    MYSQL_USER = 'root'
    MYSQL_PASS = '123456'
    MYSQL_DB   = 'humor'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': MYSQL_DB,                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASS,
        'HOST': MYSQL_HOST,                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': MYSQL_PORT,                      # Set to empty string for default.
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
#    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',    
    'humor.context_processors.global_settings',
)

SITE_NAME = "\u54a9\u54c8\u54c8\u7b11\u8bdd\u7f51"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = '' 
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static').replace('\\', '/') 

BASE_DIR = os.getcwd() 

STATICFILES_DIRS = (  
    # Put strings here, like "/home/html/static" or "C:/www/django/static".  
    # Always use forward slashes, even on Windows.  
    # Don't forget to use absolute paths, not relative paths.  
  
    os.path.join(BASE_DIR, "static"),  
) 
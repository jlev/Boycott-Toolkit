# Django settings for boycott project.

import os
SITE_ROOT = os.path.abspath(os.path.split(__file__)[0])

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Josh Levinger', 'josh@levinger.net'),
)
MANAGERS = ADMINS

#DATABASE SETTINGS
DATABASES = {
    'default': {
        "ENGINE": 'django.contrib.gis.db.backends.postgis',
        "NAME": 'boycott',
        "USER": 'josh',
        "PASSWORD": '',
        "HOST": 'localhost',
        "PORT": 5432
    }
}

#LOCALE SETTINGS
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

#STATIC SETTINGS
STATIC_ROOT = SITE_ROOT + '/static/'
STATIC_URL = 'http://boy.co.tt/static/'
ADMIN_STATIC_PREFIX = '/static/admin/'
AUTOCOMPLETE_JS_BASE_URL = STATIC_URL + "jquery/autocomplete/"

#API KEYS
SECRET_KEY=''

#REGISTRATION SETTINGS
ACCOUNT_ACTIVATION_DAYS = 7

#FACEBOOK CONNECT
FACEBOOK_API_KEY=''
FACEBOOK_SECRET_KEY=''
FACEBOOK_CACHE_TIMEOUT = 1800
FACEBOOK_INTERNAL = True
NUM_FRIEND_RETRIEVE_LIMIT = 50
DUMMY_FACEBOOK_INFO = {
    'uid':0,
    'pic':'http://static.ak.fbcdn.net/pics/t_silhouette.jpg',
    'pic_square':'http://static.ak.fbcdn.net/pics/t_silhouette.jpg',
    'profile_url': None,
    'name':'(Private)',
    'first_name':'(Private)',
    'last_name':'(Private)',
    'pic_square_with_logo':'http://static.ak.fbcdn.net/pics/t_silhouette.jpg',
    'pic_big': 'http://static.ak.fbcdn.net/pics/t_silhouette.jpg',
    'affiliations':None,
    'status':None,
    'proxied_email':None,
}

LOGIN_URL = '/community/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/community/logout/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.static",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
)

TEMPLATE_DIRS = (
    SITE_ROOT + '/templates',
    SITE_ROOT + '/olwidget/templates',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS':False #breaks facebook connect redirects
}

MIDDLEWARE_CLASSES = (
#    'debug_toolbar.middleware.DebugToolbarMiddleware', #DEBUG ONLY    
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'facebook.djangofb.FacebookMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware', 
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'facebookconnect.middleware.FacebookConnectMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
)

INTERNAL_IPS = ('127.0.0.1','18.85.45.142')

CACHE_MIDDLEWARE_SETTINGS = {'must-revalidate':True}
CACHE_BACKEND = 'memcached://127.0.0.1:11211'
CACHE_MIDDLEWARE_KEY_PREFIX = 'boycott'

AUTHENTICATION_BACKENDS = (
    #'facebookconnect.models.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'boycott.urls'
APPEND_SLASH = True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.markup',
    'django.contrib.comments',
    'django.contrib.flatpages',
    'reversion',
    'south',
    #'facebook_connect',
    'tagging',
    'autocomplete',
    'olwidget',
    'boycott.target',
    'boycott.community',
    'boycott.geography',
    'boycott.info',
#    'debug_toolbar'
)

try:
    from settings_local import *
except:
    from settings_heroku import *
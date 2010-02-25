# Django settings for boycott project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Josh Levinger', 'jlev@mit.edu'),
)
MANAGERS = ADMINS

#DATABASE SETTINGS
DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'boycott'
DATABASE_USER = 'jlev'
DATABASE_PASSWORD = ''
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'

#EMAIL SETTINGS
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'register@boy.co.tt'
EMAIL_HOST_PASSWORD = 'd3m00rd13'
EMAIL_PORT = 587

#LOCALE SETTINGS
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

#MEDIA SETTINGS
SITE_ROOT = '/Users/jlev/Code/boycott/'
MEDIA_ROOT = SITE_ROOT + 'media/'
MEDIA_URL = 'http://localhost:8000/media/'
ADMIN_MEDIA_PREFIX = '/media-admin/'
AUTOCOMPLETE_JS_BASE_URL = MEDIA_URL + "jquery/autocomplete/"

#API KEYS
SECRET_KEY = 'nvnzj@@@(rfp7r!0@-8(#*c_1wmpa7^&bxnfot_dicrg8*m4x2'

#REGISTRATION SETTINGS
ACCOUNT_ACTIVATION_DAYS = 7
#FACEBOOK CONNECT
FACEBOOK_API_KEY='ab57b2ea3e3c59f35ce7cd3905142528'
FACEBOOK_SECRET_KEY='4bdfe258832b73b2344d80ba04e7dad7'
FACEBOOK_CACHE_TIMEOUT = 1800
FACEBOOK_INTERNAL = True
NUM_FRIEND_RETRIEVE_LIMIT = 50

LOGIN_URL = '/community/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/community/logout/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)
TEMPLATE_DIRS = (
    SITE_ROOT + 'templates',
    SITE_ROOT + 'olwidget/templates',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS':False #breaks facebook connect redirects
}

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware', #DEBUG ONLY    
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'facebook.djangofb.FacebookMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware', 
    #'django.contrib.csrf.middleware.CsrfMiddleware', #doesn't play nice with facebook connect
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'facebookconnect.middleware.FacebookConnectMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

CACHE_BACKEND = 'dummy://'

AUTHENTICATION_BACKENDS = (
    'facebookconnect.models.FacebookBackend',
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
    'django_evolution',
    'reversion',
    'facebookconnect',
    'tagging',
    'autocomplete',
    'olwidget',
    'boycott.target',
    'boycott.community',
    'boycott.geography',
    'debug_toolbar'
)
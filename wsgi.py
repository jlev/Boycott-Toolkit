import sys, os

from django.core.handlers.wsgi import WSGIHandler
from django.conf import settings

os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
sys.path.insert(0, settings.SITE_ROOT)

application = WSGIHandler()
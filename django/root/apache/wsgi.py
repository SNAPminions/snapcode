from django.core.handlers.wsgi import WSGIHandler

import os
import sys

sys.stdout = sys.stderr

site = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

if site not in sys.path:
	sys.path.insert(0, site)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
application = WSGIHandler()


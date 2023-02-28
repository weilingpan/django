import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'regina_line_bot.settings'

from django.conf import settings
print(settings.INSTALLED_APPS)
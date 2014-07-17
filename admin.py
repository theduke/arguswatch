from django.contrib import admin

from .utils.django_load import load

# Piggyback off admin.autodiscover() to discover Service plugins.
load('argus_plugins')

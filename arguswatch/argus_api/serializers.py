from django.forms import widgets
from rest_framework import serializers

from ..argus_services.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id',
            'name', 'description', 'notes', 'tags',
            'parent', 'groups',
            'enabled',
            'state',
            'last_checked', 'last_ok', 'last_state_change',
        )
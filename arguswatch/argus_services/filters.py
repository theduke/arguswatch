from django import forms

import django_filters
from django_filters import filters

from .models import Service
from .plugins import ServicePlugin


class TagFilter(filters.MultipleChoiceFilter):
    @property
    def field(self):
        qs = self.model.tags.all()
        self.extra['choices'] = [(t.name, t.name) for t in qs]
        return super(TagFilter, self).field

    def filter(self, qs, value):        
        if value:
            return qs.filter(tags__name__in=value)
        
        return qs


class ServiceFilter(django_filters.FilterSet):
    plugin = filters.MultipleChoiceFilter(choices=ServicePlugin.get_plugin_choices())
    state = filters.MultipleChoiceFilter(choices=Service.STATE_CHOICES)
    tags = TagFilter()

    class Meta:
        model = Service
        fields = ['state', 'tags', 'groups', 'enabled', 'plugin']


    def __init__(self, *args, **kwargs):
        super(ServiceFilter, self).__init__(*args, **kwargs)


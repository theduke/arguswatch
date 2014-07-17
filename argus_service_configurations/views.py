from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from django_baseline.views import ListView, DetailView, CreateView, UpdateView, DeleteView, UserViewMixin

from .models import ServiceConfiguration
from .forms import ServiceConfigurationForm


class ServiceConfigurationDetailView(DetailView):
    model = ServiceConfiguration


class ServiceConfigurationListView(ListView):
    model = ServiceConfiguration
    template_name = "argus/service_configurations/service_configuration_list.html"
    extra_context = {
        'create_uri': 'argus_service_configuration_create',
        'create_label': 'New Service Configuration',
        'update_uri': 'argus_service_configuration_update',
        'delete_uri': 'argus_service_configuration_delete',
    }


class ServiceConfigurationCreateView(UserViewMixin, CreateView):
    model = ServiceConfiguration
    form_class = ServiceConfigurationForm
    extra_context = {'head_title': 'Create Service Configuration'}

    def get_success_url(self):
        return reverse('argus_service_configuration_detail', kwargs={'pk': self.object.id})


class ServiceConfigurationUpdateView(UpdateView):
    model = ServiceConfiguration
    form_class = ServiceConfigurationForm
    extra_context = {'head_title': 'Update ServiceConfiguration'}

    template_name = 'argus/service_configurations/service_configuration_update.html'


class ServiceConfigurationDeleteView(DeleteView):
    model = ServiceConfiguration
    extra_context = {'head_title': 'Delete ServiceConfiguration'}

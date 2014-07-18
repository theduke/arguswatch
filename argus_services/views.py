from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages

from django_baseline.views import ListView, DetailView, CreateView, UpdateView, DeleteView, UserViewMixin

from .models import Service, ServiceGroup
from .forms import ServiceForm, ServiceGroupForm


class ServiceGroupListView(ListView):
    model = ServiceGroup
    extra_context = {
        'create_uri': 'argus_service_group_create',
        'create_label': 'New Group',
        'update_uri': 'argus_service_group_update',
        'delete_uri': 'argus_service_group_delete',
        'page_title': 'Service Groups',
        'head_title': 'Service Groups',
    }

    template_name = 'argus/services/groups.html'


class ServiceGroupCreateView(CreateView):
    model = ServiceGroup
    form_class = ServiceGroupForm
    extra_context = {
        'head_title': 'Create Service Group',
    }
    success_url = reverse_lazy('argus_service_groups')


class ServiceGroupUpdateView(UpdateView):
    model = ServiceGroup
    form_class = ServiceGroupForm
    extra_context = {'head_title': 'Update Service Group'}
    success_url = reverse_lazy('argus_service_groups')  


class ServiceGroupDeleteView(DeleteView):
    model = ServiceGroup
    extra_context = {'head_title': 'Delete Service Group'}
    success_url = reverse_lazy('argus_service_groups')


class ServiceDetailView(DetailView):
    model = Service
    template_name = "argus/services/service_detail.html"


class ServiceListView(ListView):
    model = Service
    template_name = "argus/services/service_list.html"
    extra_context = {
        'create_uri': 'argus_service_create',
        'create_label': 'New Service',
        'update_uri': 'argus_service_update',
        'delete_uri': 'argus_service_delete',
    }


def services_list_grouped(request, slug=None):
    groups = ServiceGroup.objects.all()
    if slug:
        groups = groups.filter(slug=slug)

    groups.select_related('services')

    return render(request, 'argus/services/services_list_grouped.html', {
        'head_title': 'Services by Group',
        'page_title': 'Services by Group',
        'groups': groups,
    })


class ServiceCreateView(UserViewMixin, CreateView):
    model = Service
    form_class = ServiceForm
    extra_context = {'head_title': 'Create Service'}

    def get_success_url(self):
        return reverse('argus_service_configure', kwargs={'pk': self.object.id})


class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    extra_context = {'head_title': 'Update Service'}

    template_name = 'argus/services/service_update.html'
    success_url = reverse_lazy('argus_services')


class ServiceDeleteView(DeleteView):
    model = Service
    extra_context = {'head_title': 'Delete Service'}
    success_url = reverse_lazy('argus_services')


def configure_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    plugin = service.get_plugin()

    form_cls = plugin.form_class
    instance = service.plugin_config or plugin.config_class.objects.create()

    form = None

    if request.method == 'GET':
        form = form_cls(instance=instance)
    elif request.method == 'POST':
        form = form_cls(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save()
            service.plugin_config = obj
            service.save()

            messages.success(request, "Service {s} configuration updated.".format(s=service.name))
            return HttpResponseRedirect(reverse('argus_service_detail', kwargs={'pk': service.id}))

    return render(request, 'argus/services/service_configure.html', {
        'form': form,
        'service': service,
        'head_title': 'Configure Service - ' + str(service),
    })

## Include plugins
from .plugins.http import HttpPluginConfig

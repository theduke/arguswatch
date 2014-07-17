from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from django_baseline.views import ListView, DetailView, CreateView, UpdateView, DeleteView, UserViewMixin

from .models import Service
from .forms import ServiceForm


class ServiceDetailView(DetailView):
    model = Service


class ServiceListView(ListView):
    model = Service
    template_name = "argus/services/service_list.html"
    extra_context = {
        'create_uri': 'argus_service_create',
        'create_label': 'New Service',
        'update_uri': 'argus_service_update',
        'delete_uri': 'argus_service_delete',
    }


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


class ServiceDeleteView(DeleteView):
    model = Service
    extra_context = {'head_title': 'Delete Service'}


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

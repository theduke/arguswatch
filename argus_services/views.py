from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from django_filters.views import FilterView

from django_baseline.views import ListView, DetailView, CreateView, UpdateView, DeleteView, UserViewMixin, ExtraContextMixin

from .models import Service, ServiceGroup
from .forms import ServiceForm, ServiceGroupForm
from .filters import ServiceFilter

from ..utils.django import get_client_ip


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


class ServiceDetailView(ExtraContextMixin, DetailView):
    model = Service
    template_name = "argus/services/service_detail.html"
    extra_context = {
        'can_edit': True,
        'can_control': True,
    }


class ServiceListView(FilterView):
    filterset_class = ServiceFilter
    template_name = "argus/services/service_list.html"
    extra_context = {
        'create_uri': 'argus_service_create',
        'create_label': 'New Service',
        'update_uri': 'argus_service_update',
        'delete_uri': 'argus_service_delete',
        'can_control': True,
        'can_edit': True,
    }

    def get_context_data(self, **kwargs):
        context = super(ServiceListView, self).get_context_data(**kwargs)
        # Add model verbose name to the context if needed in template.
        context.update(self.extra_context)
        return context


def services_list_grouped(request, slug=None):
    groups = None

    if slug:
        group = get_object_or_404(ServiceGroup, slug=slug)
        groups = group.get_descendants(include_self=True)
    else:
        groups = ServiceGroup.objects.all()
    groups.select_related('services')

    filter = ServiceFilter(request.GET, queryset=groups)

    return render(request, 'argus/services/services_list_grouped.html', {
        'head_title': 'Services by Group',
        'page_title': 'Services by Group',
        'groups': groups,
        'can_control': True,
        'can_edit': True,
        'filter': filter,
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

def check_api_service_access(service):
    config = service.service_config

    if not config.passive_check_allowed:
        raise PermissionDenied("Passive checks are not enabled for this service.")

    # Check IP access restrictions.
    ips = config.get_passive_check_ips()
    if ips:
        client_ip = get_client_ip()
        if not client_ip in ips:
            raise PermissionDenied("IP is not allowed to provide passive checks.")

    # Validate api key, if one is configured.
    key = config.passive_check_api_key
    if key:
        key_get = self.request.GET.get('api-key')
        if key_get != key:
            raise PermissionDenied("Required api-key not supplied.")

def argus_api_service_event(request, pk=None, slug=None):
    service = get_object_or_404(Service, pk=pk) if pk else get_object_or_404(Service, slug=slug)
    if not service.service_config.api_can_trigger_events:
        raise PermissionDenied("API event triggering support has not been enabled for this Service")

    # TODO: add proper handling of time.

    data = request.POST if request.method == 'POST' else request.GET
    
    check_state = data.get('state')
    message = data.get('message')
    time = data.get('time')

    if not (check_state and message):
        raise Exception("state or message not supplied.")

    event = service.determine_event(check_state)
    if event:
        service.process_event(event, message)

    return HttpResponse('OK')


def service_api_passive_check(request, pk=None, slug=None):
    service = get_object_or_404(Service, pk=pk) if pk else get_object_or_404(Service, slug=slug)

    check_api_service_access(service)

    # Submitter has access to service passive check.
    # First, validate that data was supplied correctly.
    # Either: get request with GET param data
    # OR: POST request.
     
    data = None
    if request.method == 'GET':
        data = request.GET.get('data')
        if not data:
            raise Exception("GET param data not found.")
    elif request.method == 'POST':
        data = dict(request.POST)

    # Check that service actually has a passive plugin.
    if not service.get_plugin().is_passive:
        raise PermissionDenied("Service does not have a passive check configured")

    service.issue_passive_check(data)

    return HttpResponse("OK")


def run_service_check(request, pk):
    """
    Run a service check locally (in the webserver process),
    and display the result.
    """

    service = get_object_or_404(Service, id=pk)
    result = service.issue_check(run_locally=True)

    return render(request, 'argus/services/run_service_check.html', {
        'page_title': 'Check of Service ' + str(service),
        'head_title': 'Check of Service ' + str(service),
        'status': result['state'],
        'message': result['message'],
        'log': result['logs'],
        'service': service,
    })

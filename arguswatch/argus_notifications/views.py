
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from django_baseline.views import ListView, DetailView, CreateView, UpdateView, DeleteView, UserViewMixin

from ..argus_service_configurations.models import ServiceConfiguration
from .models import Notification
from .forms import NotificationForm


class NotificationDetailView(DetailView):
    model = Notification


class NotificationCreateView(UserViewMixin, CreateView):
    model = Notification
    form_class = NotificationForm
    extra_context = {'head_title': 'Create Notification'}

    def get_success_url(self):
        return reverse('argus_notification_configure', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        self.object = form.save(commit=False)

        config = get_object_or_404(ServiceConfiguration, id=self.kwargs['service_pk'])
        self.object.config = config
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())



class NotificationUpdateView(UpdateView):
    model = Notification
    form_class = NotificationForm
    extra_context = {'head_title': 'Update Notification'}

    template_name = 'argus/notifications/notification_update.html'


    def get_success_url(self):
        return reverse('argus_service_configuration_detail', 
            kwargs={'pk': self.object.config.id})


class NotificationDeleteView(DeleteView):
    model = Notification
    extra_context = {'head_title': 'Delete Notification'}

    def get_success_url(self):
        return reverse('argus_service_configuration_detail', 
            kwargs={'pk': self.object.config.id})


def configure_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    plugin = notification.get_plugin()

    form_cls = plugin.form_class
    instance = notification.plugin_config or plugin.config_class.objects.create()

    form = None

    if request.method == 'GET':
        form = form_cls(instance=instance)
    elif request.method == 'POST':
        form = form_cls(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save()
            notification.plugin_config = obj
            notification.save()

            messages.success(request, "Notification {s} configuration updated.".format(s=notification.name))
            return HttpResponseRedirect(reverse('argus_service_configuration_detail', 
                kwargs={'pk': notification.config.id}))

    return render(request, 'argus/notifications/notification_configure.html', {
        'form': form,
        'notification': notification,
        'head_title': 'Configure Notification - ' + str(notification),
    })

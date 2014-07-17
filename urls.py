from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required, login_required

from django_baseline.decorators import group_required

from .argus_services.views import ServiceListView, ServiceCreateView, ServiceDetailView, ServiceUpdateView, ServiceDeleteView
from .argus_service_configurations.views import ServiceConfigurationListView, ServiceConfigurationCreateView, ServiceConfigurationDetailView, ServiceConfigurationUpdateView, ServiceConfigurationDeleteView
from .argus_notifications.views import NotificationCreateView, NotificationDetailView, NotificationUpdateView, NotificationDeleteView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', '{{ project_name }}.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'arguswatch.views.dashboard', name='argus_dashboard'),

    ### argus_notifications ###
    url(r'^notifications/add/service/(?P<service_pk>\d+)$', NotificationCreateView.as_view(), name="argus_notification_create"),
    url(r'^notifications/notification/(?P<pk>\d+)$', NotificationDetailView.as_view(), name="argus_notification_detail"),
    url(r'^notifications/notification/(?P<pk>\d+)/edit$', NotificationUpdateView.as_view(), name="argus_notification_update"),
    url(r'^notifications/notification/(?P<pk>\d+)/delete$', NotificationDeleteView.as_view(), name="argus_notification_delete"),
    url(r'^notifications/notification/(?P<pk>\d+)/configure$', 'arguswatch.argus_notifications.views.configure_notification', name="argus_notification_configure"), 

    
    ### argus_service_configurations ###
    url(r'^service_configurations$', ServiceConfigurationListView.as_view(), name="argus_service_configurations"),
    url(r'^service_configurations/add$', ServiceConfigurationCreateView.as_view(), name="argus_service_configuration_create"),
    url(r'^service_configurations/service_configuration/(?P<pk>\d+)$', ServiceConfigurationDetailView.as_view(), name="argus_service_configuration_detail"),
    url(r'^service_configurations/service_configuration/(?P<pk>\d+)/edit$', ServiceConfigurationUpdateView.as_view(), name="argus_service_configuration_update"),
    url(r'^service_configurations/service_configuration/(?P<pk>\d+)/delete$', ServiceConfigurationDeleteView.as_view(), name="argus_service_configuration_delete"),
     

    ### argus_services ###
    url(r'^services$', ServiceListView.as_view(), name="argus_services"),
    url(r'^services/add$', ServiceCreateView.as_view(), name="argus_service_create"),
    url(r'^services/service/(?P<pk>\d+)$', ServiceDetailView.as_view(), name="argus_service_detail"),
    url(r'^services/service/(?P<pk>\d+)/edit$', ServiceUpdateView.as_view(), name="argus_service_update"),
    url(r'^services/service/(?P<pk>\d+)/delete$', ServiceDeleteView.as_view(), name="argus_service_delete"),
    url(r'^services/service/(?P<pk>\d+)/configure$', 'arguswatch.argus_services.views.configure_service', name="argus_service_configure"),
)

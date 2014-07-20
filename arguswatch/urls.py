from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required, login_required

from django_baseline.decorators import group_required

from .views import dashboard

from .argus_services.views import *
from .argus_services.views import *
from .argus_service_configurations.views import *
from .argus_notifications.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', '{{ project_name }}.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(
        r'^$', 
        permission_required('argus_services.view_service')(dashboard), 
        name='argus_dashboard'),

    ### argus_notifications ###
    url(
        r'^notifications/add/service/(?P<service_pk>\d+)$', 
        permission_required('argus_notifications.add_notification')(NotificationCreateView.as_view()),
        name="argus_notification_create"),
    url(
        r'^notifications/notification/(?P<pk>\d+)$', 
        permission_required('argus_notifications.change_notification')(NotificationDetailView.as_view()), 
        name="argus_notification_detail"),
    url(
        r'^notifications/notification/(?P<pk>\d+)/edit$', 
        permission_required('argus_notifications.change_notification')(NotificationUpdateView.as_view()), 
        name="argus_notification_update"),
    url(
        r'^notifications/notification/(?P<pk>\d+)/delete$', 
        permission_required('argus_notifications.delete_notification')(NotificationDeleteView.as_view()), 
        name="argus_notification_delete"),
    url(
        r'^notifications/notification/(?P<pk>\d+)/configure$', 
        permission_required('argus_notifications.change_notification')(configure_notification), 
        name="argus_notification_configure"), 

    
    ### argus_service_configurations ###
    url(
        r'^service_configurations$', 
        permission_required('argus_service_configurations.change_serviceconfiguration')(ServiceConfigurationListView.as_view()), 
        name="argus_service_configurations"),
    url(
        r'^service_configurations/add$', 
        permission_required('argus_service_configurations.add_serviceconfiguration')(ServiceConfigurationCreateView.as_view()), 
        name="argus_service_configuration_create"),
    url(
        r'^service_configurations/service_configuration/(?P<pk>\d+)$', 
        permission_required('argus_service_configurations.change_serviceconfiguration')(ServiceConfigurationDetailView.as_view()), 
        name="argus_service_configuration_detail"),
    url(
        r'^service_configurations/service_configuration/(?P<pk>\d+)/edit$', 
        permission_required('argus_service_configurations.change_serviceconfiguration')(ServiceConfigurationUpdateView.as_view()), 
        name="argus_service_configuration_update"),
    url(
        r'^service_configurations/service_configuration/(?P<pk>\d+)/delete$', 
        permission_required('argus_service_configurations.delete_serviceconfiguration')(ServiceConfigurationDeleteView.as_view()), 
        name="argus_service_configuration_delete"),
    
    ### argus_services ###

    # API
    
    #url(
    #    r'^api/service/(?P<pk>\d+)/passive\-check$', 
    #    service_api_passive_check, 
    #    name="argus_api_service_passive_check"),
    #url(
    #    r'^api/service/(?P<slug>[a-z0-9]+)/passive\-check$', 
    #    service_api_passive_check, 
    #    name="argus_api_service_passive_check_slugged"),

    #url(
    #    r'^api/service/(?P<pk>\d+)/event$', 
    #    argus_api_service_event, 
    #    name="argus_api_service_event"),
    #url(
    #    r'^api/service/(?P<slug>[a-z0-9]+)/event$', 
    #    argus_api_service_event, 
    #    name="argus_api_service_event"),

    ### ServiceGroup views ###
    url(
        r'^service-groups$', 
        permission_required('argus_services.change_servicegroup')(ServiceGroupListView.as_view()), 
        name="argus_service_groups"),
    url(
        r'^service-groups/create$', 
        permission_required('argus_services.add_servicegroup')(ServiceGroupCreateView.as_view()), 
        name="argus_service_group_create"),
    url(
        r'^service-groups/(?P<pk>\d+)/edit$', 
        permission_required('argus_services.change_servicegroup')(ServiceGroupUpdateView.as_view()), 
        name="argus_service_group_update"),
    url(
        r'^service-groups/(?P<pk>\d+)/delete$', 
        permission_required('argus_services.delete_servicegroup')(ServiceGroupDeleteView.as_view()), 
        name="argus_service_group_delete"),

    url(
        r'^services/grouped$', 
        permission_required('argus_services.view_service')(services_list_grouped), 
        name="argus_services_grouped_all"),
    url(
        r'^services/grouped/(?P<slug>[a-zA-Z0-9_\-]+)$', 
        permission_required('argus_services.view_service')(services_list_grouped), 
        name="argus_services_grouped"),
    url(
        r'^services$', 
        permission_required('argus_services.view_service')(ServiceListView.as_view()), 
        name="argus_services"),
    url(
        r'^services/add$', 
        permission_required('argus_services.add_service')(ServiceCreateView.as_view()), 
        name="argus_service_create"),
    url(
        r'^services/service/(?P<pk>\d+)$', 
        permission_required('argus_services.view_service')(ServiceDetailView.as_view()), 
        name="argus_service_detail"),
    url(
        r'^services/service/(?P<pk>\d+)/edit$', 
        permission_required('argus_services.change_service')(ServiceUpdateView.as_view()), 
        name="argus_service_update"),
    url(
        r'^services/service/(?P<pk>\d+)/delete$', 
        permission_required('argus_services.delete_service')(ServiceDeleteView.as_view()), 
        name="argus_service_delete"),
    url(
        r'^services/service/(?P<pk>\d+)/configure$', 
        permission_required('argus_services.change_service')(configure_service),
        name="argus_service_configure"),
    url(
        r'^services/service/(?P<pk>\d+)/run$', 
        permission_required('argus_services.run_service_check')(run_service_check), 
        name="argus_service_check"),
)

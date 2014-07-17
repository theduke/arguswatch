from django.conf.urls import patterns, include, url

from .services.views import ServiceListView, ServiceCreateView, ServiceDetailView, ServiceUpdateView, ServiceDeleteView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', '{{ project_name }}.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'core.views.home', name='home'),

    url(r'^services$', ServiceListView.as_view(), name="argus_services"),
    url(r'^services/add$', ServiceCreateView.as_view(), name="argus_service_create"),
    url(r'^services/service/(?P<pk>\d+)$', ServiceDetailView.as_view(), name="argus_service_detail"),
    url(r'^services/service/(?P<pk>\d+)/edit$', ServiceUpdateView.as_view(), name="argus_service_update"),
    url(r'^services/service/(?P<pk>\d+)/delete$', ServiceDeleteView.as_view(), name="argus_service_delete"),
    url(r'^services/service/(?P<pk>\d+)/configure$', 'arguswatch.services.views.configure_service', name="argus_service_configure"),
)

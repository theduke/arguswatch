from django import template

from arguswatch.argus_services.models import Service

register = template.Library()

# Create your own template tags here.
# Example:
#@register.simple_tag
#def add(x, y):
#  return x + y


@register.simple_tag
def get_state_class(service):
    """
    Get a css class for a Service.STATE_*.
    """

    state = service.state

    if state == Service.STATE_OK:
        return "success"
    elif state == Service.STATE_WARNING or service.state_provisional:
        return "warning"
    elif state == Service.STATE_DOWN or state == Service.STATE_UNKNOWN:
        return "danger"


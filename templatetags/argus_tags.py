from django import template

register = template.Library()

# Create your own template tags here.
# Example:
#@register.simple_tag
#def add(x, y):
#  return x + y


@register.simple_tag
def get_state_class(state):
    """
    Get a css class for a state returned by 
    Service.get_state_description()
    """

    if state == "up":
        return "success"
    elif state == "warning":
        return "warning"
    elif state == "down":
        return "danger"
    elif state == "unknown":
        return "warning"

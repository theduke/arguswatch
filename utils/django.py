import importlib

def get_cls_by_name(name):
    package = name[:name.rfind('.')]
    cls_name = name.split('.')[-1]
    module = importlib.import_module(package)

    return getattr(module, cls_name)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

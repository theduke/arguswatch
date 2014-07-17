import importlib

def get_cls_by_name(name):
    package = name[:name.rfind('.')]
    cls_name = name.split('.')[-1]
    module = importlib.import_module(package)

    return getattr(module, cls_name)

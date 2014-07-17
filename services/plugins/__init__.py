# Inspired by http://martyalchin.com/2008/jan/10/simple-plugin-framework/
import importlib

class PluginImplementationError(Exception):
    pass


class PluginCheckError(Exception):
    pass


class PluginManager(type):
    def __init__(cls, name, bases, attrs):

        if not hasattr(cls, '_plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls._plugins = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls._plugins.append(cls)


class ServicePlugin(metaclass=PluginManager):
    """
    Required attributes:

    name
    description
    config_class - the Config model for this plugin. Must inherit from arguswatch.models.ServiceConfiguration.
    form_class - the form class used for configuring the plugin.

    Required methods:

    run_check(self, config) 
    """


    __metaclass__ = PluginManager

    @classmethod
    def get_plugins(cls):
        return cls._plugins

    @classmethod
    def get_plugin_choices(cls):
        return [(plugin.__module__ + '.' + plugin.__name__, plugin.name) for plugin in cls.get_plugins()]

    name = None
    description = None
    config_class = None
    form_class = None

    def get_form_class(self):
        return self.form


    def run_check(self, config):
        """
        Perfom the actual plugin check.
        MUST throw PluginCheckError when the check fails.
        """

        msg = "Plugin {} does not implement method run_check()".format(
            self.__class__.__name__)
        raise PluginImplementationError(msg)


def get_plugin_by_name(name):
    package = name[:name.rfind('.')]
    cls_name = name.split('.')[-1]
    module = importlib.import_module(package)

    return getattr(module, cls_name)

# Inspired by http://martyalchin.com/2008/jan/10/simple-plugin-framework/

import logging


class PluginImplementationError(Exception):
    pass


class NotificationPluginConfigurationError(Exception):
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


class NotificationPlugin(metaclass=PluginManager):
    """
    Required attributes:

    name
    description
    config_class - the Config model for this plugin. Must inherit from arguswatch.models.ServiceConfiguration.
                    Needs to implement get_settings() method, which returns
                    a serializable dict used for do_notify().
                    
    form_class - the form class used for configuring the plugin.

    Required methods:

    run_check(self, config) 
    """


    __metaclass__ = PluginManager

    name = None
    description = None
    config_class = None
    form_class = None


    @classmethod
    def get_plugins(cls):
        return cls._plugins

    @classmethod
    def get_plugin_choices(cls):
        return [(plugin.__module__ + '.' + plugin.__name__, plugin.name) for plugin in cls.get_plugins()]


    def __init__(self):
        self.logger = None

    def set_logger(self, logger):
        self.looger = logger


    def get_logger(self):
        if not self.logger:
            self.logger = logging.getLogger('django')
        return self.logger

    def get_form_class(self):
        return self.form


    def build_subject_and_message(self, service, event):
        """
        Default implementation for generating a subject and message body
        for an event.
        Can be used by implementing plugins to avoid custom generation.
        """




    def do_notify(self, settings, service_data, event, old_service_data=None):
        """
        Perfom the actual plugin check.
        MUST throw PluginCheckError when the check fails.
        """

        msg = "Plugin {} does not implement method do_notify()".format(
            self.__class__.__name__)
        raise PluginImplementationError(msg)

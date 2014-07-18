# Inspired by http://martyalchin.com/2008/jan/10/simple-plugin-framework/

import logging


class PluginImplementationError(Exception):
    pass


class ServiceIsDownException(Exception):
    """
    Thrown when a plugin check concludes that the service is down.
    """
    
    def __init__(self, info, *args, **kwargs):
        self.info = info
        super(ServiceIsDownException, self).__init__(info, *args, **kwargs)


class PluginCheckError(Exception):
    """
    Thrown when a plugin check fails in some EXPECTED way.
    For example, if a website should be checked, but the checking host
    does not have an active internet connection.

    If the run_check method throws any other exception apart from 
    PluginCheckError and ServiceIsDownException, special reporting and error
    handling will commence.

    So plugins should do their best to handle known errors, and throw
    this exception with a good explenation.
    """

    def __init__(self, reason, *args, **kwargs):
        self.reason = reason
        super(PluginCheckError, self).__init__(reason, *args, **kwargs)


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
                   MUST implement get_settings() method, that returns serializable dict with settings needed
                   for running the check. This will be passed to the run_check method.
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

    def run_check(self, settings):
        """
        Perfom the actual plugin check.
        MUST throw PluginCheckError when the check fails in some way,
        and ServiceIsDownException if the service is determined to be down.
        """

        msg = "Plugin {} does not implement method run_check()".format(
            self.__class__.__name__)
        raise PluginImplementationError(msg)

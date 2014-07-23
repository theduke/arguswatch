# Inspired by http://martyalchin.com/2008/jan/10/simple-plugin-framework/

import logging

from arguswatch.argus_services.models import Service, Event


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


    def build_subject_and_message(self, service_data, event):
        """
        Default implementation for generating a subject and message body
        for an event.
        Can be used by implementing plugins to avoid custom generation.
        """

        subject = message = None

        name = service_data['name']

        last_state_change = service_data['last_state_change'].strftime('%d.%m.%Y %H:%M') if service_data['last_state_change'] else 'NEVER'
        last_ok = service_data['last_ok'].strftime('%d.%m.%Y %H:%M') if service_data['last_ok'] else 'NEVER'

        if event.event == Event.EVENT_STAYS_OK:
            subject = "Service {s} is UP".format(s=name)
            msg = "Service {s} is currently up, and has been up since {c}".format(
                s=name, c=last_state_change
            )
        elif event.event == Event.EVENT_GOES_OK:
            if event.old_state_provisional:
                subject = "Service {s} RECOVERY (soft)".format(s=name)
                msg = "Service {s} was down (soft), and CAME UP.\n".format(
                    s=name
                )
            else:
                subject = "Service {s} RECOVERY".format(s=name)
                msg = "Service {s} was down (hard), but RECOVERED, and is UP now.\n".format(
                    s=name, o=last_ok
                )
        elif event.event == Event.EVENT_GOES_DOWN_PROVISIONAL:
            subject = "Service {s} went DOWN (provisional)".format(s=name)
            msg = "Service {s} was up, but went DOWN (provisional).\nThe service was up last at: {o}".format(
                s=name, o=last_ok
            )
        elif event.event == Event.EVENT_STAYS_DOWN_PROVISIONAL:
            subject = "Service {s} stays DOWN (provisional)".format(s=name)
            msg = "Service {s} remains DOWN (provisional).\nThe service was up last at: {o}".format(
                s=name, o=last_ok
            )
        elif event.event == Event.EVENT_GOES_DOWN:
            subject = "Service {s} went DOWN".format(s=name)
            msg = "Service {s} was rechecked multiple times, but is DOWN.\nThe service was up last at: {o}".format(
                s=name, o=last_ok
            )
        elif event.event == Event.EVENT_STAYS_DOWN:
            subject = "Service {s} stays DOWN".format(s=name)
            msg = "Service {s} remains DOWN (HARD).\nThe service was up last at: {o}".format(
                s=name, o=last_ok
            )
        elif event.event == Event.EVENT_GOES_UNKNOWN_PROVISIONAL:
            subject = "Service {s} went UNKNOWN (provisional)".format(s=name)
            msg = "Service {s} was up, but went UNKNOWN (provisional).\nThe service was up last at: {o}".format(
                s=name, o=last_ok
            )
        elif event.event == Event.EVENT_STAYS_UNKNOWN_PROVISIONAL:
            subject = "Service {s} stays UNKNOWN (provisional)".format(s=name)
            msg = "Service {s} remains UNKNOWN (provisional).\nThe service was up last at: {o}".format(
                s=name, o=last_ok
            )
        elif event.event == Event.EVENT_GOES_UNKNOWN:
            subject = "Service {s} went UNKNOWN".format(s=name)
            msg = "Service {s} was rechecked multiple times, but is UNKNOWN.\nThe service was up last at: {o}".format(
                s=name, o=last_ok
            )
        elif event.event == Event.EVENT_STAYS_UNKNOWN:
            subject = "Service {s} stays UNKNOWN".format(s=name)
            msg = "Service {s} remains UNKNOWN (HARD).\nThe service was up last at: {o}".format(
                s=name, o=last_ok
            )
        elif event.event == Event.EVENT_GOES_WARNING:
            subject = "Service {s}: NEW WARNING".format(s=name)
            msg = "Service {s} changed to state WARNING.\nThe service was up last at: {o}".format(
                s=name, o=last_ok
            )
        elif event.event == Event.EVENT_STAYS_WARNING:
            subject = "Service {s} stays WARNING".format(s=name)
            msg = "Service {s} stays in state WARNING.\nThe service was up last at: {o}".format(
                s=name, o=last_ok
            )
        else:
            raise Exception("Unknown event: " + event)

        return (subject, msg)


    def do_notify(self, settings, service_data, event):
        """
        Perfom the actual plugin check.
        MUST throw PluginCheckError when the check fails.
        """

        msg = "Plugin {} does not implement method do_notify()".format(
            self.__class__.__name__)
        raise PluginImplementationError(msg)

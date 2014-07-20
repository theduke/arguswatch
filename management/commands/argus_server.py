from django.core.management.base import NoArgsCommand

from arguswatch.server import Server

class Command(NoArgsCommand):
    help = "Run the Argus server."

    def handle_noargs(self, **options):
        s = Server()
        s.run()

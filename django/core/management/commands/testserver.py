from django.core.management.base import BaseCommand

from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--verbosity', action='store', dest='verbosity', default='1',
            type='choice', choices=['0', '1', '2'],
            help='Verbosity level; 0=minimal output, 1=normal output, 2=all output'),
    )
    help = 'Runs a development server with data from the given fixture(s).'
    args = '[fixture ...]'

    requires_model_validation = False

    def handle(self, *fixture_labels, **options):
        from django.conf import settings
        from django.core.management import call_command
        from django.test.utils import create_test_db

        verbosity = int(options.get('verbosity', 1))

        # Create a test database.
        db_name = create_test_db(verbosity=verbosity)

        # Import the fixture data into the test database.
        call_command('loaddata', *fixture_labels, **{'verbosity': verbosity})

        # Run the development server. Turn off auto-reloading because it causes
        # a strange error -- it causes this handle() method to be called
        # multiple times.
        shutdown_message = '\nServer stopped.\nNote that the test database, %r, has not been deleted. You can explore it on your own.' % db_name
        call_command('runserver', shutdown_message=shutdown_message, use_reloader=False)

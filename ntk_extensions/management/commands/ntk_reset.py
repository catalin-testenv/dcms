
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections
from django.conf import settings
import shutil, os
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Resets django database and migrations for specified app (or entire project)'
    # python manage.py ntk_reset --help
    # python manage.py help ntk_reset

    def add_arguments(self, parser):
        parser.add_argument('app', nargs='?', type=str, help='Nominates which app to reset')
        parser.add_argument('--database', action='store', default=DEFAULT_DB_ALIAS, help='Nominates which database to reset default: %(default)s')

    def handle(self, *args, **options):
        app_to_reset = options.get('app')
        if app_to_reset != 'ALL' and app_to_reset not in settings.INSTALLED_APPS:
            print ('%s is not installed' % app_to_reset)
            return

        connection = connections[options.get('database')]
        connection.prepare_database()
        cursor = connection.cursor()
        tables = connection.introspection.table_names(cursor)

        # remove app tables
        try:
            for table in tables:
                if app_to_reset != 'ALL' and not table.startswith('%s_' % app_to_reset):
                    continue
                print('DROP TABLE %s' % (table,))
                try:
                    cursor.execute('DROP TABLE IF EXISTS %s CASCADE' % (table,))
                except Exception, e:
                    print(e)
        except Exception as e:
            print(e)

        # remove app models traces
        # http://www.marinamele.com/how-to-correctly-remove-a-model-or-app-in-django
        # https://fragmentsofcode.wordpress.com/2010/09/21/cleanly-removing-a-django-app/
        if app_to_reset != 'ALL':
            ContentType.objects.filter(app_label=app_to_reset).delete()  # also removes foreign entries in other django tables
            cursor.execute('DELETE FROM django_migrations WHERE app = %s ', [app_to_reset])

        cursor.close()

        # remove migration files
        for app in settings.INSTALLED_APPS:
            if app_to_reset != 'ALL' and not app == app_to_reset:
                    continue
            dir_to_look_into = os.path.join(settings.BASE_DIR, app, 'migrations')
            if os.path.isdir(dir_to_look_into):
                for the_file in os.listdir(dir_to_look_into):
                    if the_file.startswith("__init__"):
                        continue
                    file_path = os.path.join(dir_to_look_into, the_file)
                    try:
                        print('rm', file_path)
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print e

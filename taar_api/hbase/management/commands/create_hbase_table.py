from django.core.management.base import BaseCommand
from django.conf import settings
from happybase.connection import Connection


class Command(BaseCommand):
    help = 'Create a new table on HBase'

    def handle(self, *args, **options):
        conn = Connection(settings.HBASE_HOST)
        if settings.HBASE_TABLE.encode() not in conn.tables():
            self.stdout.write('Creating table "%s"...' % settings.HBASE_TABLE)
            conn.create_table(settings.HBASE_TABLE, {'cf': dict(max_versions=1)})
            self.stdout.write(
                self.style.SUCCESS('Table "%s" successfully created.' % settings.HBASE_TABLE))
        else:
            self.stdout.write(
                self.style.NOTICE('A table called "%s" already exists.' % settings.HBASE_TABLE))

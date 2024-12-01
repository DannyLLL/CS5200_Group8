from django.core.management.base import BaseCommand
import MySQLdb

class Command(BaseCommand):
    help = "Test database connection"

    def handle(self, *args, **kwargs):
        try:
            connection = MySQLdb.connect(
                host="34.19.59.91",
                user="root",
                password="200013",
                database="company",
                port=3306,
                ssl={'cert_reqs': 'CERT_NONE'}
            )
            self.stdout.write(self.style.SUCCESS("Connection successful!"))
            connection.close()
        except MySQLdb.Error as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))

import os
import mysql.connector
from mysql.connector import errorcode
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Setup database and run migrations with optional seeding'

    def add_arguments(self, parser):
        parser.add_argument(
            '--seed',
            action='store_true',
            help='Also run the seed command after setup',
        )

    def handle(self, *args, **options):
        self.stdout.write('Setting up ALX Travel App database...')

        # Create database if it doesn't exist
        self.create_mysql_database()

        # Run migrations
        self.stdout.write('Making migrations...')
        call_command('makemigrations', 'listings')

        self.stdout.write('Running migrations...')
        call_command('migrate')

        # Optionally seed database
        if options['seed']:
            self.stdout.write('Seeding database...')
            call_command('seed')

        self.stdout.write(
            self.style.SUCCESS('Database setup completed successfully!')
        )

    def create_mysql_database(self):
        """Create MySQL database if it doesn't exist"""
        db_config = settings.DATABASES['default']

        db_name = db_config['NAME']
        db_user = db_config['USER']
        db_password = db_config['PASSWORD']
        db_host = db_config['HOST']
        db_port = db_config['PORT']

        try:
            # Connect without specifying database
            cnx = mysql.connector.connect(
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            cursor = cnx.cursor()

            # Check if database exists
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
            if cursor.fetchone():
                self.stdout.write(f"Database '{db_name}' already exists.")
            else:
                self.stdout.write(f"Creating database '{db_name}'...")
                cursor.execute(
                    f"CREATE DATABASE {db_name} CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'"
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Database '{db_name}' created successfully!")
                )

            cursor.close()
            cnx.close()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.stdout.write(
                    self.style.ERROR("Access denied: Check username/password")
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f"MySQL Error: {err}")
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Unexpected error: {e}")
            )

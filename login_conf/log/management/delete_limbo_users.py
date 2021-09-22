# delete_limbo_users.py
import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Delete registered but unactive users older than the given number of days.'

    def add_arguments(self, parser):
        parser.add_argument('days', type=int, help='Retention period in days.')

    def handle(self, *args, **options):
        days = options['days']

        print('-------------------------------------------')
        print('| Checking limbo users older than: %s days |' % days)
        print('-------------------------------------------')

        retention_period = datetime.timedelta(days)
        expiry_date = datetime.date.today() - retention_period

        deleted_users = 0
        unactive_users = User.objects.filter(is_active = 0)
        for user in unactive_users:
            if user.date_joined.date() < expiry_date:
                print('>> Deleting user: : %s -- %s' % (user.username, user.date_joined))
                user.delete()
                deleted_users = deleted_users + 1
        
        if deleted_users == 0:
            print('>> No users to be deleted')

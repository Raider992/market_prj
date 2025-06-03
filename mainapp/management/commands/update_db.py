from django.core.management import BaseCommand

from authapp.models import TravelUser, TravelUserProfile


class Command(BaseCommand):
    help = 'update DB'

    def handle(self, *args, **options):
        users = TravelUser.objects.all()
        for user in users:
            users_profile = TravelUserProfile.objects.create(user=user)
            users_profile.save()
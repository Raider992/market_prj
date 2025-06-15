from django.core.management import BaseCommand

from authapp.models import TravelUser, TravelUserProfile


class Command(BaseCommand):
    help = 'update DB'

    def handle(self, *args, **options):
        users = TravelUser.objects.all()
        user_profiles = TravelUserProfile.objects.all()
        profile_id_list = []

        for profile in user_profiles:
            profile_id_list += profile.user_id

        for user in users:
            if user.id not in profile_id_list:
                users_profile = TravelUserProfile.objects.create(user=user)
                users_profile.save()
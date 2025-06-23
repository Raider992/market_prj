from datetime import date
from http.cookiejar import month
from urllib.parse import urlencode
from urllib.parse import urlunparse
from django.utils import timezone
from social_core.exceptions import AuthForbidden
import requests
from .models import TravelUser, TravelUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if not isinstance(user, TravelUser):
        return

    if backend.name != 'google-oauth2':
        return

    api_url = urlunparse((
        'https',
        'people.googleapis.com',
        '/v1/people/me',
        None,
        urlencode({
            'personFields': 'genders,birthdays,biographies',
            'access_token': response['access_token']
        }),
        None
    ))

    resp = requests.get(api_url)

    if resp.status_code != 200:
        print(f"Ошибка при получении данных от Google API: {resp.status_code} - {resp.text}")
        return

    data = resp.json()
    try:
        user_profile = user.traveluserprofile
    except TravelUserProfile.DoesNotExist:
        user_profile = TravelUserProfile.objects.create(user=user)

    if 'genders' in data and data['genders']:
        gender_data = data['genders'][0]
        if 'value' in gender_data:
            if gender_data['value'].lower() == 'male':
                user_profile.gender = TravelUserProfile.MALE
            elif gender_data['value'].lower() == 'female':
                user_profile.gender = TravelUserProfile.FEMALE

    if 'biographies' in data and data['biographies']:
        about_me_data = data['biographies'][0]
        if 'value' in about_me_data:
            user_profile.aboutMe = about_me_data['value'][:512]

    if 'birthdays' in data and data['birthdays']:
        birthday_data = data['birthdays'][0]
        if 'date' in birthday_data:
            bdate_dict = birthday_data['date']
            try:
                year = bdate_dict.get('year')
                month = bdate_dict.get('month')
                day = bdate_dict.get('day')
                if year and month and day:
                    today = date.today()
                    age = today.year - year - ((today.month, today.day) < (month,day))

                    if age < 18:
                        user.delete()
                        raise AuthForbidden('social_core.backends.google.GoogleOAuth2')

                    user.age = age
            except ValueError as e:
                print(f"Ошибка парсинга даты рождения: {e}")
                pass

    user_profile.save()
    user.save()
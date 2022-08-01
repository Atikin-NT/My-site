from django.contrib.auth.models import User
from article.models import Profile
from datetime import datetime
import requests
from niktech import settings

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        # добавить поиск по email

        if Profile.objects.filter(user_id=user.id).exists():
            profile = Profile.objects.filter(user_id=user.id)[0]
        else:
            profile = Profile(user=user)

        # avatar
        file = open(f"{settings.MEDIA_ROOT}/users/{profile.user.id}_{profile.user.username}.png", "wb")
        image_url = requests.get(response.get('photo'))
        file.write(image_url.content)
        file.close()

        profile.avatar = f"users/{profile.user.id}_{profile.user.username}.png"

        profile.save()

    if backend.name == 'google-oauth2':
        if Profile.objects.filter(user_id=user.id).exists():
            profile = Profile.objects.filter(user_id=user.id)[0]
        else:
            profile = Profile(user=user)

        file = open(f"{settings.MEDIA_ROOT}/users/{profile.user.id}_{profile.user.username}.png", "wb")
        image_url = requests.get(response.get('picture'))
        file.write(image_url.content)
        file.close()

        profile.avatar = f"users/{profile.user.id}_{profile.user.username}.png"

        profile.save()

    if backend.name == 'github':
        if Profile.objects.filter(user_id=user.id).exists():
            profile = Profile.objects.filter(user_id=user.id)[0]
        else:
            profile = Profile(user=user)

        file = open(f"{settings.MEDIA_ROOT}/users/{profile.user.id}_{profile.user.username}.png", "wb")
        image_url = requests.get(response.get('avatar_url'))
        file.write(image_url.content)
        file.close()

        profile.avatar = f"users/{profile.user.id}_{profile.user.username}.png"

        profile.save()

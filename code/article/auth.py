from article.models import Profile
from datetime import datetime
import requests
from niktech import settings

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':

        user.username = response.get('first_name')
        user.save()

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
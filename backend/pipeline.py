import requests
from django.core.files.base import ContentFile


def save_github_profile(backend, user, response, *args, **kwargs):
    """
    Пайплайн для сохранения дополнительных данных из профиля GitHub.
    """
    if backend.name != 'github':
        return

    # GitHub возвращает URL аватарки
    avatar_url = response.get('avatar_url')

    # скачиваем её и сохраняем в поле модели
    if avatar_url and not user.avatar:
        img_response = requests.get(avatar_url)
        if img_response.status_code == 200:
            # Сохраняем картинку в поле avatar
            user.avatar.save(
                f'{user.username}_github_avatar.jpg',
                ContentFile(img_response.content),
                save=False
            )

    name = response.get('name')
    if name and not user.first_name:
        user.first_name = name

    # Сохраняем обновленные данные пользователя
    user.save()
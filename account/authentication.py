from django.contrib.auth.models import User


class EmailAuthBackend:
    """
    Аутентифицировать посредством адреса электронной почты.
    """

    # поиск пользователя с подходящими данными
    def authenticate(self, request, username=None, password=None):

        try:
            user = User.objects.get(email=username)
            # сверение хешей паролей
            if user.check_password(password):
                return user
            return None
        # если пользователей много или нет ошибка
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    # исп аут пользователя бэкенда, что бы получить объект User
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

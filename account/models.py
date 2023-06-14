from django.conf import settings
from django.db import models


# Create your models here.

class Profile(models.Model):

    # указываем класс модели с которой устанавливаем связь через сетиннги
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    # upload_to указывает куда сохранять изображения
    photo = models.ImageField(upload_to='users/%Y/%m/%d',
                              blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

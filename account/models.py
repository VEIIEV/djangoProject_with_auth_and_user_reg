from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    # магия Джанго для изменения модели при изменении модели User
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

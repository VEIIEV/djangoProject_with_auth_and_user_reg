from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image


# декоратор принимает отправителя и список сигналов которые нужно применить
@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()

# связь функции с сигналом происходит в конфиге приложения

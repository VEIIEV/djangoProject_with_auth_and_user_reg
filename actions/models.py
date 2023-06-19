
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# обобщённые отношения позволяют одну модель комментариев
# использовать для связи с неопределённо большим кругом заранее неизвестных моделей.

class Action(models.Model):
    user = models.ForeignKey('auth.User',
                             related_name='actions',
                             on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    # создание обобщенной связи
    # поле ForeignKey, указывающие на модель ContentType
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='Target_obj',
                                  on_delete=models.CASCADE,  # limit_choices_to=
                                  )
    # поле, хранит первичный ключ связанного объекта
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True)
    # реализации связи на основе 2 верхних полей
    # джанго не создает это поле в БД, поэтому индекс по нему не сделаешь
    target = GenericForeignKey('target_ct', 'target_id')


class Meta:
    indexes = [
        models.Index(fields=['-created']),  # 1
        models.Index(fields=['target_ct', 'target_id'])  # 2 (состоит из 2 полей)
    ]
    ordering = ['-created']

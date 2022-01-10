from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Notification(models.Model):

    type = models.CharField(default='dialog', max_length=30)
    reciever = models.ForeignKey(User, verbose_name='Получатель', on_delete=models.CASCADE, related_name='notifications',
                                 blank=True, null=True)
    text = models.TextField(verbose_name='Текст сообщения', max_length=1300)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE,
                               blank=True, null=True)
    read = models.BooleanField(default=False, verbose_name='Прочитанно', db_index=True)
    verb = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    deleted = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.timestamp

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'


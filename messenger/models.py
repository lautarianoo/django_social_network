from django.contrib.auth import get_user_model
from django.db import models
import uuid
from profiles.models import PhotosUser

User = get_user_model()

class Dialog(models.Model):
    '''ДИАЛОГ МЕЖДУ ДВЕМЯ ЛЮДЬМИ'''

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user1 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user1_dialog', blank=True, null=True)
    user2 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user2_dialog', blank=True, null=True)

    def __str__(self):
        return f"{self.user1} | {self.user2}"

    class Meta:
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'

class Conference(models.Model):
    '''БЕСЕДА'''

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    members = models.ManyToManyField(User, related_name='conference_member', blank=True)
    admins = models.ManyToManyField(User, related_name='conference_admin', blank=True)
    title = models.CharField(max_length=150, verbose_name='Название')
    avatar = models.ImageField(verbose_name='Аватар беседы')
    slug = models.SlugField(verbose_name='Технический слаг', unique=True)

    def __str__(self):
       return f"{self.id} | {self.title}"

    def save(self, *args, **kwargs):
        new_slug = "c{}".format(self.id)
        self.slug = new_slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Беседа'
        verbose_name_plural = 'Беседы'

class Message(models.Model):

    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='messages', null=True, blank=True)
    text = models.TextField()
    images = models.ManyToManyField(PhotosUser, related_name='image_messages', blank=True)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name='messages_dialog', null=True, blank=True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='messages_conference', null=True, blank=True)
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} | {self.date_add}"

    @classmethod
    def is_conference(cls):
        if Conference.objects.filter(messages_conference=cls):
            return True
        return False

    @classmethod
    def is_dialog(cls):
        if Dialog.objects.filter(messages_conference=cls):
            return True
        return False

    class Meta:

        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

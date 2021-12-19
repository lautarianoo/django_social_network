from django.contrib.auth import get_user_model
from django.db import models
import uuid
from profiles.models import PhotosUser

User = get_user_model()


class Room(models.Model):
    '''БЕСЕДА'''

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    members = models.ManyToManyField(User, related_name='conference_member', blank=True)
    admins = models.ManyToManyField(User, related_name='conference_admin', blank=True)
    title = models.CharField(max_length=150, verbose_name='Название', blank=True, null=True)
    avatar = models.ImageField(verbose_name='Аватар беседы', blank=True, null=True)
    conference = models.BooleanField(verbose_name='Конференция', default=False)
    slug = models.SlugField(verbose_name='Технический слаг', unique=True)

    def __str__(self):
       return f"{self.id} | {self.title}"

    def save(self, *args, **kwargs):
        new_slug = "c{}".format(self.id)
        self.slug = new_slug
        super().save(*args, **kwargs)

    def last_message(self):
       return self.messages_room.last()

    class Meta:
        verbose_name = 'Беседа'
        verbose_name_plural = 'Беседы'

class Message(models.Model):

    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='messages', null=True, blank=True)
    text = models.TextField()
    images = models.ManyToManyField(PhotosUser, related_name='image_messages', blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages_room', null=True, blank=True)
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} | {self.date_add}"

    @classmethod
    def is_conference(cls):
        if Room.objects.filter(messages_conference=cls, conference=True):
            return True
        return False

    @classmethod
    def is_dialog(cls):
        if Room.objects.filter(messages_conference=cls, conference=False):
            return True
        return False

    class Meta:

        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

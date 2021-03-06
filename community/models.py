import sys
import random
from django.contrib.auth import get_user_model
from django.db import models
from feed.models import Feed
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

User = get_user_model()

class CategoryGroup(models.Model):

    title = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class InfoGroup(models.Model):

    status = models.CharField(max_length=250, verbose_name='Статус группы')
    privaty = models.BooleanField(verbose_name='Закрытая группа', default=False)
    description = models.TextField(verbose_name='Описание', max_length=1200)
    website = models.CharField(verbose_name='Сайт сообщества', max_length=200)
    contacts = models.ManyToManyField('profiles.SocialUser', verbose_name='Контакты', related_name='infogroup')

    class Meta:
        verbose_name = 'Информация о группе'
        verbose_name_plural = 'Информации о группах'

class Group(models.Model):

    category = models.ForeignKey(CategoryGroup, verbose_name='Категория группы', on_delete=models.CASCADE,
                                 related_name='groups')
    title = models.CharField(max_length=120, verbose_name='Название группы')
    thematic = models.CharField(verbose_name='Тематика группы', max_length=100)
    photos = models.ManyToManyField('profiles.PhotosUser', verbose_name='Фотографии', related_name='group', blank=True)
    author = models.ForeignKey(User, verbose_name='Автор группы', on_delete=models.SET_NULL, null=True, related_name='groupss')
    feeds = models.ManyToManyField(Feed, verbose_name='Лента новостей', related_name='group', blank=True)
    followers = models.ManyToManyField(User, verbose_name='Участники', related_name='group', blank=True)
    applications = models.ManyToManyField(User, verbose_name='Заявки на вступление', related_name='app_group', blank=True)
    infogroup = models.ForeignKey(InfoGroup, verbose_name='Информация', related_name='groups', on_delete=models.SET_NULL, null=True)
    avatar = models.ImageField(verbose_name='Аватар группы')
    banned = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    slug = models.CharField(max_length=120, verbose_name='Прозвище группы', blank=True, null=True)

    def save(self, *args, **kwargs):
        #
        if self.avatar:
            image = self.avatar
            img = Image.open(image)
            new_img = img.convert('RGB')
            resized_new_img = new_img.resize((200, 200), Image.ANTIALIAS)
            filestream = BytesIO()
            resized_new_img.save(filestream, 'JPEG', quality=90)
            filestream.seek(0)
            name = '{}.{}'.format(*self.avatar.name.split('.'))
            self.avatar = InMemoryUploadedFile(
                filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

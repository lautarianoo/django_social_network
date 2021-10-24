import sys

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

    PRIVATY_STATUS = (
        ('Открытая', 'open'),
        ('Закрытая', 'privat')
    )

    status = models.CharField(max_length=250, verbose_name='Статус группы')
    privaty = models.CharField(verbose_name='Приватность', max_length=30, choices=PRIVATY_STATUS)
    description = models.CharField(verbose_name='Описание', max_length=1200)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Информация о группе'
        verbose_name_plural = 'Информации о группах'

class Group(models.Model):

    THEMATICS = (
        ('Образование', 'edu'),
        ('Техника', 'tech'),
        ('Авто/Мото', 'auto'),
        ('Услуги', 'service'),
        ('Блог', 'blog'),
        ('Другое', 'other')
    )
    category = models.ForeignKey(CategoryGroup, verbose_name='Категория группы', on_delete=models.SET_NULL, null=True,
                                 related_name='groups')
    title = models.CharField(max_length=120, verbose_name='Название группы')
    thematic = models.CharField(verbose_name='Тематика группы', max_length=100, choices=THEMATICS)
    website = models.CharField(verbose_name='Сайт сообщества', max_length=200)
    author = models.ForeignKey(User, verbose_name='Автор группы', on_delete=models.SET_NULL, null=True, related_name='groupss')
    feeds = models.ManyToManyField(Feed, verbose_name='Лента новостей', related_name='group')
    followers = models.ManyToManyField(User, verbose_name='Подписчики', related_name='group')
    infogroup = models.ForeignKey(InfoGroup, verbose_name='Информация', related_name='groups', on_delete=models.SET_NULL, null=True)
    avatar = models.ImageField(verbose_name='Аватар группы')

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
        return f"{self.title} | {self.author.username}"

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

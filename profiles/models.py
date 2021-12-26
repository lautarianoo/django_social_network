from ckeditor.fields import RichTextField
from django.db import models

# Create your models here.
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from feed.models import Feed

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Comments(models.Model):

    author = models.ForeignKey('SocialUser', verbose_name='Автор комментария', on_delete=models.CASCADE,
                               related_name='comments2')
    parents = models.ManyToManyField('self', verbose_name='Родитель', related_name='comment2')
    content = RichTextField(blank=True, null=True, verbose_name='Контент', max_length=1150)
    likes = models.IntegerField(verbose_name='Лайки комментария', default=0)
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Автор id: {self.author.id} | {self.date_add}"

class PhotosUser(models.Model):

    image = models.ImageField(verbose_name='Фотография')
    likes = models.IntegerField(verbose_name='Лайки фотографии', default=0)
    comments = models.ManyToManyField(Comments, verbose_name='Комментарии к фотографии', blank=True, related_name='photo')
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.image:
            image = self.image
            img = Image.open(image)
            new_img = img.convert('RGB')
            resized_new_img = new_img.resize((700, 400), Image.ANTIALIAS)
            filestream = BytesIO()
            resized_new_img.save(filestream, 'JPEG', quality=90)
            filestream.seek(0)
            name = '{}.{}'.format(*self.image.name.split('.'))
            self.image = InMemoryUploadedFile(
                filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
            )
        super().save(*args, **kwargs)

class InfoUser(models.Model):

    birthday = models.CharField(verbose_name='День рождения', max_length=11, blank=True, null=True)
    city = models.CharField(verbose_name='Город', max_length=30, blank=True, null=True)
    status = models.CharField(verbose_name='Статус профиля', max_length=88, blank=True, null=True)
    work = models.CharField(verbose_name='Работа', max_length=60, blank=True, null=True)

    class Meta:
        verbose_name = 'Информация о юзере'
        verbose_name_plural = 'Информации'

class FollowersUser(models.Model):
    followers = models.ManyToManyField(
        'SocialUser',
        verbose_name="Подписчик",
        blank=True,
        related_name='owner')

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self):
        return "{}".format(self.id)

class SubscribersUser(models.Model):
    subscribers = models.ManyToManyField(
        'SocialUser',
        verbose_name="Подписота",
        blank=True,
        related_name='owner2')

    class Meta:
        verbose_name = "Подписота"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return "{}".format(self.id)

class SocialUser(AbstractBaseUser):

    first_name = models.CharField(verbose_name='Имя', max_length=35)
    last_name = models.CharField(verbose_name='Фамилия', max_length=40)
    email = models.EmailField(verbose_name='Почта', unique=True)
    phone = models.CharField(verbose_name='Телефон', max_length=18)
    infouser = models.ForeignKey(InfoUser, verbose_name='Информация о юзере', on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    feeds = models.ManyToManyField(Feed, verbose_name='Лента юзера', related_name='user', blank=True)
    status_email = models.BooleanField(verbose_name='Email подтверждён', default=False)
    avatar = models.ImageField(verbose_name='Аватар', blank=True, null=True)
    friends = models.ManyToManyField('self', verbose_name='Друзья', related_name='user', blank=True)
    followers = models.ForeignKey(FollowersUser, verbose_name='Подписчики', on_delete=models.CASCADE, blank=True, null=True)
    subscribers = models.ForeignKey(SubscribersUser, verbose_name='Подписки', on_delete=models.CASCADE, blank=True, null=True)
    photos = models.ManyToManyField(PhotosUser, verbose_name='Фотографии', related_name='user', blank=True)
    videos = models.FileField(upload_to='files/', blank=True, null=True)
    username = models.CharField(verbose_name='Никнейм', unique=True, max_length=40, null=True)
    groups = models.ManyToManyField('community.Group', verbose_name='Группы', related_name='user', blank=True)
    full_name = models.CharField(verbose_name='Полное имя', max_length=75, blank=True, null=True)
    date_add = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyUserManager()

    def __str__(self):
        return f"{self.first_name} | {self.last_name}"


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
        self.full_name = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователя'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

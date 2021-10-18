from django.db import models

# Create your models here.
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


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

class PhotosUser(models.Model):

    image = models.ImageField(verbose_name='Фотография')

    def __str__(self):
        return self.id

class InfoUser(models.Model):
    pass

class SocialUser(AbstractBaseUser):

    first_name = models.CharField(verbose_name='Имя', max_length=35)
    last_name = models.CharField(verbose_name='Фамилия', max_length=40)
    email = models.EmailField(verbose_name='Почта')
    status_email = models.BooleanField(verbose_name='Email подтверждён', default=False)
    avatar = models.ImageField(verbose_name='Аватар', blank=True, null=True)
    friends = models.ManyToManyField('self', verbose_name='Подписчики', related_name='user')
    followers = models.ManyToManyField('self', verbose_name='Подписчики', related_name='user')
    photos = models.ManyToManyField(PhotosUser, verbose_name='Фотографии', related_name='user')
    videos = models.FileField(upload_to='files/', blank=True, null=True)
    username = models.CharField(verbose_name='Прозвище/Слаг', unique=True)
    date_add = models.DateTimeField(auto_now_add=True)




    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyUserManager()

    def __str__(self):
        return f""

    def save(self, *args, **kwargs):
        #
        if self.avatar:
            image = self.avatar
            img = Image.open(image)
            new_img = img.convert('RGB')
            resized_new_img = new_img.resize((150, 150), Image.ANTIALIAS)
            filestream = BytesIO()
            resized_new_img.save(filestream, 'JPEG', quality=90)
            filestream.seek(0)
            name = '{}.{}'.format(*self.avatar.name.split('.'))
            self.avatar = InMemoryUploadedFile(
                filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
            )
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

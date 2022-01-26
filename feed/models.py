from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Comment(models.Model):

    author = models.ForeignKey('profiles.SocialUser', verbose_name='Автор комментария', on_delete=models.CASCADE,
                               related_name='comments')
    parents = models.ManyToManyField('profiles.SocialUser', verbose_name='Родитель', related_name='comment')
    content = RichTextUploadingField(blank=True, null=True, verbose_name='Контент', max_length=1150)
    likes = models.IntegerField(verbose_name='Лайки комментария', default=0)
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Автор id: {self.author.id} | {self.date_add}"


class Feed(models.Model):

    content = RichTextUploadingField(blank=True, null=True, verbose_name='Контент', max_length=7000)
    images = models.ManyToManyField('profiles.PhotosUser', verbose_name='Фотографии', blank=True)
    comments = models.ManyToManyField(Comment, verbose_name='Комментарии', related_name='feed')
    bgroup = models.BooleanField(verbose_name='Группа', default=False)
    likes = models.IntegerField(default=0, verbose_name='Кол-во лайков')
    date_add = models.DateTimeField(auto_now_add=True)
    reposted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

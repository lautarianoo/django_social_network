from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Feed(models.Model):

    author = models.ForeignKey('profiles.SocialUser', verbose_name='Автор', on_delete=models.SET_NULL)
    content = RichTextUploadingField()
    likes = models.IntegerField(default=0, verbose_name='Кол-во лайков')
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} | {self.id}"

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

from django.contrib import admin
from .models import Feed, Comment
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class FeedAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Feed
        fields = ('__all__')

class FeedAdmin(admin.ModelAdmin):
    form = FeedAdminForm

class CommentAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Comment
        fields = ('__all__')

class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm


admin.site.register(Feed, FeedAdmin)
admin.site.register(Comment, CommentAdmin)

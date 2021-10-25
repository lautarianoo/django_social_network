from django.contrib import admin
from .models import InfoGroup, Group, CategoryGroup

admin.site.register(Group)
admin.site.register(InfoGroup)
admin.site.register(CategoryGroup)

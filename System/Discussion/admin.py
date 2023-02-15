from django.contrib import admin

from .models import DiscGroup, DiscRecord, LikeRecord

# Register your models here.

admin.site.register(DiscGroup)
admin.site.register(DiscRecord)
admin.site.register(LikeRecord)
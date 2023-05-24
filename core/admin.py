from django.contrib import admin

# Register your models here.
from.models import KanBanBoard, Lane, Tags, Card, Comment

admin.site.register(KanBanBoard)
admin.site.register(Lane)
admin.site.register(Tags)
admin.site.register(Card)
admin.site.register(Comment)

from django.contrib import admin
from .models import Article, TimeCheck

# Register your models here.
admin.site.register(Article)
admin.site.register(TimeCheck)
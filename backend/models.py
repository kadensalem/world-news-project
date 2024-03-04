from django.db import models

# Create your models here.
class Article(models.Model):
    source = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    urlToImage = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    
class TimeCheck(models.Model):
    time = models.DateTimeField()
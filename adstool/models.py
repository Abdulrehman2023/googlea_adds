from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Template(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    info = models.JSONField()
    logo = models.ImageField(upload_to="templates/", default="ads/logo.png")
    product = models.ImageField(upload_to="templates/", default="ads/product.png")
    x300x50 = models.ImageField(upload_to="templates/",null=True,blank=True)
    x320x50 = models.ImageField(upload_to="templates/",null=True,blank=True)
    x728x90 = models.ImageField(upload_to="templates/",null=True,blank=True)
    x160x600 = models.ImageField(upload_to="templates/",null=True,blank=True)
    x300x250 = models.ImageField(upload_to="templates/",null=True,blank=True)
    x300x600 = models.ImageField(upload_to="templates/",null=True,blank=True)
    x320x100 = models.ImageField(upload_to="templates/",null=True,blank=True)
    x320x480 = models.ImageField(upload_to="templates/",null=True,blank=True)
    x970x250 = models.ImageField(upload_to="templates/",null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

class FontCategory(models.Model):
    category = models.CharField(max_length=50)

class FontFamily(models.Model):
    category = models.ForeignKey(FontCategory,on_delete=models.CASCADE)
    family = models.CharField(max_length=50)
    files = models.JSONField()


class Ads(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(Template,on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    info = models.JSONField()
    logo = models.ImageField(upload_to="ads/assets/", default="ads/logo.png")
    product = models.ImageField(upload_to="ads/assets/", default="ads/product.png")
    x300x50 = models.ImageField(upload_to="ads/",null=True,blank=True)
    x320x50 = models.ImageField(upload_to="ads/",null=True,blank=True)
    x728x90 = models.ImageField(upload_to="ads/",null=True,blank=True)
    x160x600 = models.ImageField(upload_to="ads/",null=True,blank=True)
    x300x250 = models.ImageField(upload_to="ads/",null=True,blank=True)
    x300x600 = models.ImageField(upload_to="ads/",null=True,blank=True)
    x320x100 = models.ImageField(upload_to="ads/",null=True,blank=True)
    x320x480 = models.ImageField(upload_to="ads/",null=True,blank=True)
    x970x250 = models.ImageField(upload_to="ads/",null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

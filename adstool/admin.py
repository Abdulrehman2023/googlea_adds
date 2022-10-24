from django.contrib import admin
from adstool import models
# Register your models here.
admin.site.register(models.Template)
admin.site.register(models.Ads)
admin.site.register(models.FontCategory)
admin.site.register(models.FontFamily)
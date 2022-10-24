from django.contrib import admin
from app import models
from django.utils.html import format_html
# Register your models here.
# class CampaignAdmin(admin.ModelAdmin):
# 	# def delete(self, obj):
# 	# 	return format_html(f'<a class="btn" href="/admin/app/campaign/{obj.pk}/delete/">Delete</a>')
# 	# delete.allow_tags = True
# 	# delete.short_description = 'Delete object'
# 	# list_display = ['Name','completed','create_at','delete']
# 	# list_editable = ['completed']
admin.site.register(models.Campaign)

class ClientUrlAdmin(admin.ModelAdmin):
	list_display = ['Url', 'category','create_at']
	search_fields = ['Url']
	list_filter = ['category']
admin.site.register(models.ClientUrl,ClientUrlAdmin)

# class DeviceAdmin(admin.ModelAdmin):
# 	list_display = ['device','Type','w','h','create_at']
# admin.site.register(models.Device,DeviceAdmin)

class CampaignImagesAdmin(admin.ModelAdmin):
	list_display = ['url','campaign','device','created_at']
admin.site.register(models.CampaignImages,CampaignImagesAdmin)

class ContactAdmin(admin.ModelAdmin):
	list_display = ['email','firstname','lastname','created_at']
admin.site.register(models.Contact,ContactAdmin)

class UserSubscritionAdmin(admin.ModelAdmin):
	list_display = ['user','status','create_at']
admin.site.register(models.UserSubscription,UserSubscritionAdmin)

class Subscription_planAdmin(admin.ModelAdmin):
	list_display = ['Name','price','lookup_key','duration']
admin.site.register(models.Subscription_plan,Subscription_planAdmin)
admin.site.register(models.UrlImage)
admin.site.register(models.Size)
admin.site.register(models.Result)
admin.site.register(models.CompaignUpload)
admin.site.register(models.CompainUploadSize)



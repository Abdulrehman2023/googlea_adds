# from django.db import modelstgres
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

# class Device(models.Model):
#     devices=(
#         ("Mobile","Mobile"),
#         ("Desktop","Desktop")
#     )
#     type=(
#         ("Image","Image"),
#         ("Video","Video")
#     )
#     device = models.CharField(max_length=50,choices=devices)
#     Type = models.CharField(max_length=50,choices=type)
#     w = models.PositiveIntegerField()
#     h = models.PositiveIntegerField()
#     create_at = models.DateTimeField(auto_now=True)

#     # def __str__(self):
#     #     return self.device+" "+self.Type+" "+str(self.Width)+"x"+str(self.Height)
class Catogries(models.TextChoices):
    VIDEO  = 'VIDEO','Video'
    ARTS = 'ARTS','Arts & Entertainment'
    AUTO = 'AUTO','Auto'
    BEAUTY = 'BEAUTY','Beauty & Fitness'
    BOOKS = 'BOOKS','Books & Literature'
    BUSSINESS = 'BUSSINESS','Business & Industry'
    FINANCE = 'FINANCE','Finance'
    FOOD = 'FOOD','Food & Drink'
    GAMING = 'GAMING','Gaming'
    HEALTH = 'HEALTH','Health'
    HOBBY = 'HOBBY','Hobbys & Interests'
    HOME = 'HOME','Home & Garden'
    INERNET = 'INERNET','Internet & Telcom'
    JOBS = 'JOBS','Jobs & Education'
    LAW = 'LAW','Law & Government'
    NEWS = 'NEWS','News'
    COMMUNITIES = 'COMMUNITIES','Online Communities'
    PEOPLE = 'PEOPLE','People & Society'
    PERFORMANCE = 'PERFORMANCE','Performance'
    PETS = 'PETS','Pets & Animals'
    REALESTATE = 'REALESTATE','Realestate'
    REFERENCE = 'REFERENCE','Reference'
    SCIENCE = 'SCIENCE','Science'
    SHOPPING = 'SHOPPING','Shopping'
    SPORTS = 'SPORTS','Sports'
    TRAVEL = 'TRAVEL','Travel'
    WORLD = 'WORLD','World Localities'


class ClientUrl(models.Model):
    category = models.CharField(max_length=50,choices=Catogries.choices)
    Url = models.URLField()
    create_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Url

class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    Name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)

class CompaignUpload(models.Model):
    Campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="campaignuploads/")
    created_at = models.DateTimeField(auto_now=True)

class CompainUploadSize(models.Model):
    campaignupload = models.ForeignKey(CompaignUpload,on_delete=models.CASCADE)
    size = models.ForeignKey("Size",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

class CampaignImages(models.Model):
    campaign = models.ForeignKey(Campaign,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="CampaignImages/")
    device = models.CharField(max_length=30)
    url = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)

class Result(models.Model):
    URL = models.ForeignKey("UrlImage",on_delete=models.CASCADE)
    image = models.ImageField(upload_to="results/")

class Subscription_plan(models.Model):
    Name = models.CharField(max_length=255)
    price = models.CharField(max_length=10)
    lookup_key = models.CharField(max_length=20)
    duration = models.PositiveIntegerField(help_text="Duration in months")
    stripe_product_id = models.CharField(max_length=255)
    stripe_price_id = models.CharField(max_length=255)

class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Subscription_plan,on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=True)
    session_id = models.CharField(max_length=250)
    customer = models.CharField(max_length=255)
    amount_total = models.CharField(max_length=10)
    subscription = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255)
    started_at = models.DateTimeField()
    end_at = models.DateTimeField()
    create_at = models.DateTimeField(auto_now=True)

class Contact(models.Model):
    email = models.CharField(max_length=100)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

class UrlImage(models.Model):
    URL = models.ForeignKey(ClientUrl,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="screenshots/")
    def __str__(self):
        return self.URL.Url

class Size(models.Model):
    urlimage= models.ForeignKey(UrlImage,on_delete=models.CASCADE)
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    def __str__(self):
        return f'{self.weight}x{self.height}'
    


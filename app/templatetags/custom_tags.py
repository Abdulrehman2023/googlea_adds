import os
from django import template
from app import models
from project import settings
s3 = settings.BotoClient

register = template.Library()
@register.filter(name="screenshot")
def screenshot(value):
    return models.CampaignImages.objects.filter(campaign__id=value).count()

@register.filter(name="range")
def screenshot(value):
    objects = s3.list_objects(Bucket="piranhad", Prefix=f"{value}/")
    objects_keys = {'Objects' : []}
    objects_keys['Objects'] = [{'Key' : k} for k in [obj['Key'] for obj in objects.get('Contents', [])]]
    return range(len(objects_keys['Objects']))

@register.filter(name="img")
def img(value,args):
    objects = s3.list_objects(Bucket="piranhad", Prefix=f"{args}/")
    objects_keys = {'Objects' : []}
    objects_keys['Objects'] = [{'Key' : k} for k in [obj['Key'] for obj in objects.get('Contents', [])]]
    return objects_keys['Objects'][value]['Key'].split('/')[1]

@register.filter(name="created")
def created(value,args):
    objects = s3.list_objects(Bucket="piranhad", Prefix=f"{args}/")
    objects_keys = {'Objects' : []}
    objects_keys['Objects'] = [{'LastModified' : k} for k in [obj['LastModified'] for obj in objects.get('Contents', [])]]
    return objects_keys['Objects'][value]['LastModified']

    # lista = os.listdir('media/{}/'.format(args))
    # return time.ctime(os.path.getctime('media/{}/{}'.format(args,lista[value])))

@register.filter(name="detail")
def detail(value,args):
    value = value.split("__")
    return value[args]

@register.filter(name="clean_url")
def clean_url(url):
    return url.replace("www.","")


@register.filter(name="noofsizes")
def noofsizes(value):
    size = []
    obj = models.ClientUrl.objects.get(pk=value)
    for i in obj.ads:
        size.append(f"({int(i['w'])}x{int(i['h'])})")
    size = list(dict.fromkeys(size))
    return range(len(size))

@register.filter(name="sizes")
def sizes(value,args):
    size = []
    obj = models.ClientUrl.objects.get(pk=value)
    for i in obj.ads:
        size.append(f"({int(i['w'])}x{int(i['h'])})")
    size = list(dict.fromkeys(size))
    return size[args]


@register.filter(name="mysizes")
def sizes(value):
    size = []
    obj = models.Size.objects.filter(urlimage__URL__pk=value).values('weight','height')
    
    print("-------------------------")
    print(obj)
    lst = [f"{i['weight']}x{i['height']}" for i in obj]
    
    return tuple(lst)

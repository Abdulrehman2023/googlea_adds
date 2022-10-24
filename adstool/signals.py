from random import randint
import shutil,os
from django.dispatch import receiver
from django.db.models import signals
from adstool import models
import math,cv2,requests
from PIL import ImageFont,ImageDraw, Image,ImageColor
from adstool import modules
from django.core.files import File
from urllib.request import urlopen
from project import settings

def url_to_image(url):
    try:
        img_data = requests.get(url).content
        name = randint(0,1000)
        with open(f'media/{name}.png', 'wb') as handler:
            handler.write(img_data)
        return True, f'media/{name}.png'
    except:
        return False, "Connection error occured! Please try again.Thank you"

@receiver(signals.post_save, sender=models.Template)
def create_template(sender, instance, created, *args, **kwargs):
    if created:
        if not os.path.exists(f"media/templates/{instance.id}"):
            os.makedirs(f"media/templates/{instance.id}")
        for i in instance.info['sizes'].keys():
            width,height = i.split('x')
            width,height = int(width),int(height)
            blank_image = Image.new("RGBA", (width, height), ImageColor.getcolor(instance.info['ad']['background'], "RGB"))
            blank_image.save(f"media/templates/{instance.id}/{i}.png")
            if 'logoimg' in instance.info['sizes'][i]:
                img1 = Image.open(f"media/templates/{instance.id}/{i}.png")
                status, logo = url_to_image(f"{settings.MEDIA_URL}{instance.logo}")
                if status:
                    img2 = Image.open(logo).convert("RGBA")
                    cords = instance.info['sizes'][i]['logoimg']
                    x,y,w,h = cords['x'],cords['y'],cords['w'],cords['h']
                    img2 = img2.resize((w,h))
                    img1.paste(img2, (x,y), mask = img2)
                    img1.save(f"media/templates/{instance.id}/{i}.png")
                    os.remove(logo)
            if 'productimg' in instance.info['sizes'][i]:
                img1 = Image.open(f"media/templates/{instance.id}/{i}.png")
                status, productimg = url_to_image(f"{settings.MEDIA_URL}{instance.product}")
                if status:
                    product = Image.open(productimg).convert("RGBA")
                    cords = instance.info['sizes'][i]['productimg']
                    x,y,w,h = cords['x'],cords['y'],cords['w'],cords['h']
                    product = product.resize((w,h))
                    img1.paste(product, (x,y), mask = product)
                    img1.save(f"media/templates/{instance.id}/{i}.png")
                    os.remove(productimg)
            if 'ctabutton' in instance.info['sizes'][i]:
                blank_image = cv2.imread(f"media/templates/{instance.id}/{i}.png")
                cords = instance.info['sizes'][i]['ctabutton']
                x,y,w,h = cords['x'],cords['y'],cords['w'],cords['h']
                blank_image[y:y+h,x:x+w] = modules.color(instance.info['ad']['ctabutton'],"grb")
                cv2.imwrite(f"media/templates/{instance.id}/{i}.png",blank_image)
                img = Image.open(f"media/templates/{instance.id}/{i}.png")
                I1 = ImageDraw.Draw(img)
                cta = instance.info['ad']['cta']
                myFont = ImageFont.truetype(urlopen(cta['style']), cta['size'])
                line_width, line_height =x+math.floor((w - myFont.getsize(cta['text'])[0])/2) , y+math.floor((h - myFont.getsize(cta['text'])[1])/2)
                I1.text((line_width, line_height), cta['text'], font=myFont, fill=ImageColor.getcolor(cta['color'], "RGB"))
                img.save(f"media/templates/{instance.id}/{i}.png")
            if 'headline' in instance.info['sizes'][i]:
                cords = instance.info['sizes'][i]['headline']
                x,y,w,h = cords['x'],cords['y'],cords['w'],cords['h']
                img = Image.open(f"media/templates/{instance.id}/{i}.png")
                headline = instance.info['ad']['headline']
                myFont = ImageFont.truetype(urlopen(headline['style']), headline['size'])
                modules.draw_multiple_line_text(img, headline['text'], myFont, modules.color(headline['color'],"brg"), y,w,x)
                img.save(f"media/templates/{instance.id}/{i}.png")
            if 'subhead' in instance.info['sizes'][i]:
                cords = instance.info['sizes'][i]['subhead']
                x,y,w,h = cords['x'],cords['y'],cords['w'],cords['h']
                img = Image.open(f"media/templates/{instance.id}/{i}.png")
                subhead = instance.info['ad']['subhead']
                myFont = ImageFont.truetype(urlopen(subhead['style']), subhead['size'])
                modules.draw_multiple_line_text(img, subhead['text'], myFont, modules.color(subhead['color'],"brg"), y,w,x)
                img.save(f"media/templates/{instance.id}/{i}.png")
            setattr(instance,f"x{i}",File(file=open(f"media/templates/{instance.id}/{i}.png", "rb"),name="{}.png".format(str(hex(randint(0, 16777215)))[2:])))
        instance.save()
        shutil.rmtree(f"media/templates/{instance.id}")

@receiver(signals.post_delete, sender=models.Template)
def delete_template(sender, instance, *args, **kwargs):
    if os.path.exists(f"media/templates/{instance.id}"):
        shutil.rmtree(f"media/templates/{instance.id}")
    instance.logo.delete(save=False)
    instance.product.delete(save=False)
    instance.x300x50.delete(save=False)
    instance.x320x50.delete(save=False)
    instance.x728x90.delete(save=False)
    instance.x160x600.delete(save=False)
    instance.x300x250.delete(save=False)
    instance.x300x600.delete(save=False)
    instance.x320x100.delete(save=False)
    instance.x320x480.delete(save=False)
    instance.x970x250.delete(save=False)

@receiver(signals.post_save, sender=models.Ads)
def create_ads(sender, instance,created, *args, **kwargs):
    if created:
        if not os.path.exists(f"media/ads/{instance.id}"):
            os.makedirs(f"media/ads/{instance.id}")
        for i in instance.info['sizes'].keys():
            width,height = i.split('x')
            width,height = int(width),int(height)
            blank_image = Image.new("RGBA", (width, height), ImageColor.getcolor(instance.info['ad']['background'], "RGB"))
            blank_image.save(f"media/ads/{instance.id}/{i}.png")
            if 'logoimg' in instance.info['sizes'][i]:
                img1 = Image.open(f"media/ads/{instance.id}/{i}.png")
                status, logo = url_to_image(f"{settings.MEDIA_URL}{instance.logo}")
                if status:
                    img2 = Image.open(logo).convert("RGBA")
                    cords = instance.info['sizes'][i]['logoimg']
                    x,y,w,h = cords['x'],cords['y'],cords['w'],cords['h']
                    img2 = img2.resize((w,h))
                    img1.paste(img2, (x,y), mask = img2)
                    img1.save(f"media/ads/{instance.id}/{i}.png")
                    os.remove(logo)
            if 'productimg' in instance.info['sizes'][i]:
                img1 = Image.open(f"media/ads/{instance.id}/{i}.png")
                status, productimg = url_to_image(f"{settings.MEDIA_URL}{instance.product}")
                if status:
                    product = Image.open(productimg).convert("RGBA")
                    cords = instance.info['sizes'][i]['productimg']
                    x,y,w,h = cords['x'],cords['y'],cords['w'],cords['h']
                    product = product.resize((w,h))
                    img1.paste(product, (x,y), mask = product)
                    img1.save(f"media/ads/{instance.id}/{i}.png")
                    os.remove(productimg)
            if 'ctabutton' in instance.info['sizes'][i]:
                blank_image = cv2.imread(f"media/ads/{instance.id}/{i}.png")
                cords = instance.info['sizes'][i]['ctabutton']
                x,y,w,h = cords['x'],cords['y'],cords['w'],cords['h']
                blank_image[y:y+h,x:x+w] = modules.color(instance.info['ad']['ctabutton'],"grb")
                cv2.imwrite(f"media/ads/{instance.id}/{i}.png",blank_image)
                img = Image.open(f"media/ads/{instance.id}/{i}.png")
                I1 = ImageDraw.Draw(img)
                cta = instance.info['ad']['cta']
                myFont = ImageFont.truetype(urlopen(cta['style']), cta['size'])
                line_width, line_height =x+math.floor((w - myFont.getsize(cta['text'])[0])/2) , y+math.floor((h - myFont.getsize(cta['text'])[1])/2)
                I1.text((line_width, line_height), cta['text'], font=myFont, fill=ImageColor.getcolor(cta['color'], "RGB"))
                img.save(f"media/ads/{instance.id}/{i}.png")
            if 'headline' in instance.info['sizes'][i]:
                cords = instance.info['sizes'][i]['headline']
                x,y,w,h = cords['x'],cords['y'],cords['w'],cords['h']
                img = Image.open(f"media/ads/{instance.id}/{i}.png")
                headline = instance.info['ad']['headline']
                myFont = ImageFont.truetype(urlopen(headline['style']), headline['size'])
                modules.draw_multiple_line_text(img, headline['text'], myFont, modules.color(headline['color'],"brg"), y,w,x)
                img.save(f"media/ads/{instance.id}/{i}.png")
            if 'subhead' in instance.info['sizes'][i]:
                cords = instance.info['sizes'][i]['subhead']
                x,y,w,h = cords['x'],cords['y'],cords['w'],cords['h']
                img = Image.open(f"media/ads/{instance.id}/{i}.png")
                subhead = instance.info['ad']['subhead']
                myFont = ImageFont.truetype(urlopen(subhead['style']), subhead['size'])
                modules.draw_multiple_line_text(img, subhead['text'], myFont, modules.color(subhead['color'],"brg"), y,w,x)
                img.save(f"media/ads/{instance.id}/{i}.png")
            setattr(instance,f"x{i}",File(file=open(f"media/ads/{instance.id}/{i}.png", "rb"),name="{}.png".format(str(hex(randint(0, 16777215)))[2:])))
        instance.save()
        shutil.rmtree(f"media/ads/{instance.id}")

@receiver(signals.post_delete, sender=models.Ads)
def delete_ads(sender, instance, *args, **kwargs):
    if os.path.exists(f"media/ads/{instance.id}"):
        shutil.rmtree(f"media/ads/{instance.id}")
    if not instance.logo.name == "ads/logo.png":
        instance.logo.delete(save=False)
    if not instance.product.name == "ads/product.png":
        instance.product.delete(save=False)
    instance.x300x50.delete(save=False)
    instance.x320x50.delete(save=False)
    instance.x728x90.delete(save=False)
    instance.x160x600.delete(save=False)
    instance.x300x250.delete(save=False)
    instance.x300x600.delete(save=False)
    instance.x320x100.delete(save=False)
    instance.x320x480.delete(save=False)
    instance.x970x250.delete(save=False)
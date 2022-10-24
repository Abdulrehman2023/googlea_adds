import json,os,math,textwrap,cv2,boto3,shutil,numpy as np
from random import randint
from PIL import ImageFont,ImageDraw, Image, ImageColor
from urllib.request import urlopen
from adstool import signals
from project import settings
from django.core.files import File
s3 = boto3.client('s3')
#  AIzaSyDgc5ff26tiXw83XnkuFGgecAP7wb6a_14
# https://www.googleapis.com/webfonts/v1/webfonts?key=AIzaSyDgc5ff26tiXw83XnkuFGgecAP7wb6a_14
def color(val,mode):
    val = val.lstrip('#')
    b,r,g = tuple(int(val[i:i+2], 16) for i in (0, 2, 4))
    if mode == "brg":
        return (b,r,g)
    if mode == "grb":
        return (g,r,b)

def draw_multiple_line_text(image, text, font, text_color, y,w,x):
    draw = ImageDraw.Draw(image)
    lines = textwrap.wrap(text, width=w)
    for line in lines:
        draw.text((x, y), line, font=font, fill=text_color)
        y += font.getsize(line)[1]

def update_ads(instance):
    images_keys = []
    product = cv2.imread(f'media/{instance.product}')
    if not os.path.exists(f"media/ads/{instance.id}"):
        os.makedirs(f"media/ads/{instance.id}")
    for i in instance.info['sizes'].keys():
        width,height = i.split('x')
        width,height = int(width),int(height)
        blank_image = Image.new("RGBA", (width, height), ImageColor.getcolor(instance.info['ad']['background'], "RGBA"))        
        blank_image.save(f"media/ads/{instance.id}/{i}.png")
        if 'logoimg' in instance.info['sizes'][i]:
            img1 = Image.open(f"media/ads/{instance.id}/{i}.png")
            status, logo = signals.url_to_image(f"{settings.MEDIA_URL}{instance.logo}")
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
            status, productimg = signals.url_to_image(f"{settings.MEDIA_URL}{instance.product}")
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
            blank_image[y:y+h,x:x+w] = color(instance.info['ad']['ctabutton'],"grb")
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
            draw_multiple_line_text(img, headline['text'], myFont, color(headline['color'],"brg"), y,w,x)
            img.save(f"media/ads/{instance.id}/{i}.png")
        if 'subhead' in instance.info['sizes'][i]:
            cords = instance.info['sizes'][i]['subhead']
            x,y,w,h = cords['x'],cords['y'],cords['w'],cords['h']
            img = Image.open(f"media/ads/{instance.id}/{i}.png")
            subhead = instance.info['ad']['subhead']
            myFont = ImageFont.truetype(urlopen(subhead['style']), subhead['size'])
            draw_multiple_line_text(img, subhead['text'], myFont, color(subhead['color'],"brg"), y,w,x)
            # shape = [(x, y), (x+w, y+h)]
            # img1 = ImageDraw.Draw(img)
            # img1.rectangle(shape,outline ="red")
            img.save(f"media/ads/{instance.id}/{i}.png")
        images_keys.append({'Key' : f"staticfiles/{getattr(instance,f'x{i}')}"})
        setattr(instance,f"x{i}",File(file=open(f"media/ads/{instance.id}/{i}.png", "rb"),name="{}.png".format(str(hex(randint(0, 16777215)))[2:])))
    delete_keys = {'Objects' : []}
    delete_keys['Objects'] = images_keys
    if delete_keys['Objects']:
        s3.delete_objects(Bucket="piranhad", Delete=delete_keys)
    instance.save()
    shutil.rmtree(f"media/ads/{instance.id}")

# import requests
# from adstool import models
# def Googlefonts():
#     url = "https://www.googleapis.com/webfonts/v1/webfonts?key=AIzaSyDgc5ff26tiXw83XnkuFGgecAP7wb6a_14"
#     resp = requests.get(url)
#     data = json.loads(resp.content.decode())
#     for i in data['items']:
#         obj, created = models.FontCategory.objects.get_or_create(category=i['category'])
#         models.FontFamily.objects.get_or_create(category=obj, family=i['family'], defaults={
#         "files" : i['files']
#         })

# Googlefonts()
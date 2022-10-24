from os.path import dirname
import zipfile
from django.http import HttpResponse
from django_xhtml2pdf.utils import generate_pdf
from celery import shared_task
from PyPDF2 import PdfMerger
from django.core.files import File
import requests,random,cv2,os,time
from app import models
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
from botocore.exceptions import ClientError
from project import settings
from selenium.common.exceptions import WebDriverException
import pdf2docx, shutil 
from pdf2docx import Converter
import subprocess
from selenium import webdriver
import base64
import time
import os
import codecs
from selenium.webdriver.common.by import By
from threading import Thread
from multiprocessing import Process
import cv2
import math
from PIL import Image, ImageDraw
import string
import random
from selenium.webdriver.chrome.options import Options
import glob
import numpy as np
from selenium.common.exceptions import WebDriverException

s3 = settings.BotoClient

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--log-level=3")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
CHROMEDRIVER_PATH="C:\\Users\\FabTechSol\\Downloads\\chromedriver_win32\\chromedriver.exe"
driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

def pdf(obj):
    try:
        context = {}
        resp = HttpResponse(content_type='application/pdf')
        merger = PdfMerger()
        merger.write(f'media/pdf/{obj.id}.pdf')
        merger.close()
        obj.errors.append("Preparing ZIP")
        obj.save()
        obj.zip.save("{}.zip".format(obj.id), File(open(f"media/zip/{obj.id}.zip", "rb")))
        obj.errors.append("Preparing PDF")
        obj.save()
        qs = models.CampaignImages.objects.filter(campaign__id=obj.id).order_by('created_at')
        for i in qs:
            if i.image:
                merger = PdfMerger()
                context['obj'] = i
                result = generate_pdf('app/generate_pdf.html', file_object=resp, context=context)
                with open(f'media/pdf/{obj.id}{i.id}.pdf', 'wb') as f:
                    f.write(result.content)
                for pdf in [f'media/pdf/{obj.id}.pdf',f'media/pdf/{obj.id}{i.id}.pdf']:
                    print(f"Merging {pdf}")
                    merger.append(pdf)
                os.remove(os.path.join(settings.BASE_DIR/"media", f"pdf/{obj.id}{i.id}.pdf"))
                os.remove(os.path.join(settings.BASE_DIR/"media", f"pdf/{obj.id}.pdf"))
                merger.write(f'media/pdf/{obj.id}.pdf')
                merger.close()
        obj.pdf.save("{}.pdf".format(obj.id), File(open(f"media/pdf/{obj.id}.pdf", "rb")))
        obj.save()
        # shutil.make_archive(f"media/zip/{obj.id}", 'zip', f'media/{obj.id}')
        # try:
        #     cv = Converter(os.path.join(settings.BASE_DIR / "media", "pdf/{}.pdf".format(obj.id)))
        #     cv.convert(os.path.join(settings.BASE_DIR / "media", "word/{}.docx".format(obj.id)))
        #     cv.close()
        #     obj.word.save("{}.docx".format(obj.id), File(open(f"media/word/{obj.id}.docx", "rb")))
        # except Exception as e:
        #     print(e)
        # fl = subprocess.run(["pdf2pptx",f"media/pdf/{obj.id}.pdf",f"-o media/pptx/{obj.id}.pptx"])
        # obj.pptx.save("{}.pptx".format(obj.id), File(open(f"media/pptx/{obj.id}.pptx", "rb")))
        # os.system(f"pdf2pptx media/pdf/{obj.id}.pdf -o media/pptx/{obj.id}.pptx")
        # pdf2docx.parse(f'media/pdf/{obj.id}.pdf', f'media/word/{obj.id}.docx')

        print("saved!")
    except Exception as e:
        print(e)

def check(value):
	objects = s3.list_objects(Bucket="piranhad", Prefix=f"{value}/")
	objects_keys = {'Objects' : []}
	objects_keys['Objects'] = [{'Key' : k} for k in [obj['Key'] for obj in objects.get('Contents', [])]]
	return range(len(objects_keys['Objects']))

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = settings.BotoClient
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def url_to_image(url):
    try:
        img_data = requests.get(url).content
        with open(f'media/temp.png', 'wb') as handler:
            handler.write(img_data)
        return True, f'media/temp.png'
    except:
        return False, "Connection error occured! Please try again.Thank you"

def get_src(src):
    coords = []
    for el in src:
        x,y = el.location.values()
        h, w = el.size.values()
        coords.append((x,y,w,h))
    return max(coords)

def place_Ad(obj,qs,device,zip_obj):
    for q in qs:
        draw = False
        status,img = url_to_image(f'{settings.MEDIA_URL}{q.image}')
        if status:
            img = cv2.imread(img)
        else:
            obj.errors.append(img)
            obj.save()
            continue
        rand = q.image.name.replace('screenshots/','')
        adsign  = cv2.imread(f'media/adsign.png')
        for j in obj.AdFile:
            ad  = cv2.imread(f'media/{obj.id}_ads/{j}')
            for a in q.ads:
                try:
                    x,y,h,w = int(a['x']),int(a['y']),int(a['h']),int(a['w'])
                    if w == int(ad.shape[1]) and h == int(ad.shape[0]):
                        if device == "Desktop":
                            if obj.desktopdevices.filter(w = int(ad.shape[1]), h = int(ad.shape[0])).exists():
                                try:
                                    img[y:y+h,x:x+w] = ad
                                except ValueError as e:
                                    obj.errors.append(f'Not processed {q.Url.split("://")[1].split("/")[0].replace("www.","")}')
                                    obj.save()
                                    continue
                                img[y:y+int(adsign.shape[0]),x+w-int(adsign.shape[1]):x+w] = adsign
                                draw = True
                        if device == "Mobile":
                            if obj.mobiledevices.filter(w = int(ad.shape[1]), h = int(ad.shape[0])).exists():
                                try:
                                    img[y:y+h,x:x+w] = ad
                                except ValueError as e:
                                    obj.errors.append(f'Not processed {q.Url.split("://")[1].split("/")[0].replace("www.","")}')
                                    obj.save()
                                    continue
                                img[y:y+int(adsign.shape[0]),x+w-int(adsign.shape[1]):x+w] = adsign
                                draw = True
                except:
                    obj.errors.append(f'Not processed {q.Url.split("://")[1].split("/")[0].replace("www.","")}')
                    obj.save()
                    continue

        if draw:
            url = q.Url.split("://")[1].split("/")[0].replace("www.","")
            name = 'media/{}/{}__{}__{}'.format(obj.id,url,q.device,rand)
            cv2.imwrite(name,img)
            # s3.upload_file(name, 'piranhad','{}/{}__{}__{}'.format(obj.id,url,q.device,rand))
            zip_obj.write(name,"{}__{}__{}".format(url,q.device,rand))
            cpn = models.CampaignImages.objects.create(campaign=obj,device=q.device,url=url)
            cpn.image.save("{}__{}__{}".format(url,q.device,rand), File(open(name, "rb")))
            os.remove(name)
            
    return True, "Generated"

def place_video_ad(obj,zip_obj):
    try:
        for q in obj.CampaignUrl.all():
            draw = False
            status,img = url_to_image(f'{settings.MEDIA_URL}{q.image}')
            if status:
                img = cv2.imread(img)
            else:
                obj.errors.append(img)
                obj.save()
                continue
            rand = q.image.name.replace('screenshots/','')
            ad  = cv2.imread(f'media/{obj.id}_ads/{obj.AdFile[0].rsplit(".")[0]}.png')
            videosign  = cv2.imread(f'media/video_layer.png')
            a = q.ads[0]
            try:
                x,y,h,w = int(a['x']),int(a['y']),int(a['h']),int(a['w'])
                dim = (w,h)
                ad = cv2.resize(ad, dim, interpolation = cv2.INTER_AREA)
                videosign = cv2.resize(videosign, dim, interpolation = cv2.INTER_AREA)
                ad = cv2.addWeighted(ad, 1, videosign, 1, 0)                        
                img[y:y+h,x:x+w] = ad
                img = img[:y+h+20,:int(img.shape[1])]
                draw = True
            except:
                obj.errors.append(f'Not processed {q.Url.split("://")[1].split("/")[0].replace("www.","")}')
                obj.save()
                continue
            if draw:
                url = q.Url.split("://")[1].split("/")[0]
                name = 'media/{}/{}__{}__{}'.format(obj.id,url,q.device,rand)
                cv2.imwrite(name,img)
                # s3.upload_file(name, 'piranhad','{}/{}__{}__{}.png'.format(obj.id,url,q.device,rand))
                zip_obj.write(name,"{}__{}__{}".format(url,q.device,rand))
                cpn = models.CampaignImages.objects.create(campaign=obj,device=q.device,url=url)
                cpn.image.save("{}__{}__{}".format(url,q.device,rand), File(open(name, "rb")))
                os.remove(name)
        return True, f"Success Thank you."
    except Exception as e:
        print(e)
        obj.errors.append(f"Unexpected Error occured! Please try again.")
        obj.save()
        return False, f"Oops! Could not connect with {q.Url.split('://')[1].split('/')[0]}! Please try again. Thank you."

# @shared_task(time_limit=21600)
def capturess(*args):
    sites=['https://animalfactguide.com/']

    for site in sites:

        try:
            driver.get(site)


            print("page loadded")
            time.sleep(15)

            getstyle = driver.find_elements(By.TAG_NAME, 'iframe')
            result = []

            def apply_style(s,element):
                    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",element, s)

            def highlight(element, effect_time, color, border):
                """Highlights (blinks) a Selenium Webdriver element"""
                driver = element._parent
                original_style = element.get_attribute('style')
                apply_style("border: {0}px solid {1};".format(border, color),element)
                time.sleep(effect_time)
                driver.save_screenshot('screenshot.png')
                apply_style(original_style,element)


            for style in getstyle:
                iframe = style.get_attribute("name")
                if "google_ads_iframe" in iframe:
                    print("-------------------------------")
                    print(style)
                    a = style.get_attribute("name")
                    result.append(a)
                    print(style.get_attribute("name"))
                    print(style.get_attribute("height"))
                    width= style.get_attribute("width")
                    print(width)
                
                    print(style.get_attribute("style"))
                    if width !='':
                        content = driver.find_element(By.ID, a)
                        driver = content._parent
                        driver.execute_script("arguments[0].scrollIntoView(true);", content);
                        highlight(content, 5, 'red', 2)
                        img = Image.open('screenshot.png')
                        rimg = img.copy()
                        name=site[8:-1]
                        making_name = name+'pic'+'_'+str(flag)
                        flag = flag+1
                        saved_name='./scraped_images'+'/'+making_name+'.png'                     
                        rimg.save(saved_name)
                    print("-------------------------------")
                elif "aswift" in iframe:
                    print("-------------------------------")
                    print(style)
                    a = style.get_attribute("name")
                    result.append(a)
                    print(style.get_attribute("name"))
                    print(style.get_attribute("height"))
                    width=style.get_attribute("width")
                    print(style.get_attribute("style"))

                    print(width)
                    if width !='':
                        content = driver.find_element(By.ID, a)
                        driver = content._parent
                        driver.execute_script("arguments[0].scrollIntoView(true);", content);
                        highlight(content, 5, 'red', 3)
                        img = Image.open('screenshot.png')
                        rimg = img.copy()
                        name=site[8:-1]
                        making_name = name+'pic'+'_'+str(flag)
                        flag = flag+1
                        saved_name='./scraped_images'+'/'+making_name+'.png'                     
                        rimg.save(saved_name)
                    print("-------------------------------")
                else:
                    print('no add found')



            

            def opencv_handler(img):
                # Read input image
                get_image = img
                img = cv2.imread(img)
            

                # Gel all pixels in the image - where BGR = (34, 33, 33), OpenCV colors order is BGR not RGB
                gray = np.all(img == (0, 0, 255), 2)  # gray is a logical matrix with True where BGR = (34, 33, 33).

                # Convert logical matrix to uint8
                gray = gray.astype(np.uint8)*255

                # Find contours
                cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # Use index [-2] to be compatible to OpenCV 3 and 4

                # Get contour with maximum area
                c = max(cnts, key=cv2.contourArea)

                x, y, w, h = cv2.boundingRect(c)
                print(get_image+'=',w,h)
                
                
                


            screenshots =glob.glob("scraped_images*/*.png")
            print(screenshots) 


            for image in screenshots:
                if site[8:-1] in image:
                    opencv_handler(image)
        

        except WebDriverException:
            print("page down")

def save_frames(video_path: str, frame_dir: str, sec, ext="png"):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return
    if frame_dir[-1:] == "\\" or frame_dir[-1:] == "/":
        frame_dir = dirname(frame_dir)
    base_path = frame_dir
    idx = 0
    while cap.isOpened():
        idx += 1
        ret, frame = cap.read()
        if ret:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == 1:  #Save 0 second frame
                if int(sec) == 0:
                    cv2.imwrite("{}.{}".format(base_path, ext), frame)
                    return "{}/{}.{}".format(base_path,ext)
            elif idx < cap.get(cv2.CAP_PROP_FPS):
                continue
            else:  #Save frames 1 second at a time
                second = int(cap.get(cv2.CAP_PROP_POS_FRAMES)/idx)
                if second == int(sec):
                    cv2.imwrite("{}.{}".format(base_path, ext), frame)
                    return "{}.{}".format(base_path, ext)
                idx = 0
        else:
            break

def DownloadFromURL(image_url):
    uid = str(hex(random.randint(0, 16777215)))[2:]
    img_data = requests.get(image_url).content
    with open(f'media/{uid}.png', 'wb') as handler:
        handler.write(img_data)
    return f'media/{uid}.png'


def create_devices():
	devices = [
		{
			'device': 'Mobile',
            'Type': 'Image',
			'w': 300,
            'h': 50
		},
		{
			'device': 'Mobile',
            'Type': 'Image',
			'w': 300,
            'h': 250
		},
		{
			'device': 'Mobile',
            'Type': 'Image',
			'w': 320,
            'h': 50
		},
		{
			'device': 'Mobile',
            'Type': 'Image',
			'w': 320,
            'h': 480
		},


		{
			'device': 'Desktop',
            'Type': 'Image',
			'w': 160,
            'h': 600
		},
		{
			'device': 'Desktop',
            'Type': 'Image',
			'w': 300,
            'h': 250
		},
		{
			'device': 'Desktop',
            'Type': 'Image',
			'w': 300,
            'h': 600
		},
		{
			'device': 'Desktop',
            'Type': 'Image',
			'w': 320,
            'h': 100
		},
		{
			'device': 'Desktop',
            'Type': 'Image',
			'w': 320,
            'h': 480
		},
        {
			'device': 'Desktop',
            'Type': 'Image',
			'w': 728,
            'h': 90
		},
		{
			'device': 'Desktop',
            'Type': 'Image',
			'w': 970,
            'h': 250
		}
	]

	# for i in devices:
	# 	models.Device.objects.get_or_create(**i)


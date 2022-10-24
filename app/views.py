from datetime import timedelta
import json, os, magic,stripe
from django.http import HttpResponse, JsonResponse
from django.shortcuts import  render, redirect
from django.views import View
from http import HTTPStatus
from app import models,forms,signals,tasks
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm #add this
from django.contrib.auth import login, authenticate, logout #add this
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.db.models import F
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes,force_str
from project import settings
from app.token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
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



options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--log-level=3")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
CHROMEDRIVER_PATH="C:\\Users\\FabTechSol\\Downloads\\chromedriver_win32\\chromedriver.exe"
options.add_argument("window-size=1400,800")
driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
flag=1
url_image_id =0
# stripe.api_key = settings.stripe_key

# domain = settings.domain
# mime = magic.Magic(mime=True)
# # module.create_devices()
# errormsg = ""
# errorstatus = False

def errormsgupdate(msg):
	global errormsg, errorstatus
	errormsg = msg
	errorstatus = True
	return redirect('ServerError')

class ServerError(View):
	def get(self,request, *args, **kwargs):
		global errormsg, errorstatus
		response = render(request,'app/error_page.html',{"message":errormsg})
		errormsg = ""
		errorstatus = False
		response.status_code = 500
		return response

def handler404(request, *args, **argv):
    response = render(request,'app/404.html')
    response.status_code = 404
    return response
def handler500(request, *args, **argv):
    response = render(request,'app/500.html')
    response.status_code = 500
    return response

if not os.path.exists('staticfiles'):
	os.makedirs('staticfiles')
if not os.path.exists('media/pdf'):
	os.makedirs('media/pdf')
if not os.path.exists(f'media/word'):
	os.makedirs(f'media/word')
if not os.path.exists(f'media/pptx'):
	os.makedirs(f'media/pptx')
if not os.path.exists(f'media/zip'):
	os.makedirs(f'media/zip')
	
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "app/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':domain,
					'site_name': 'Piranhad',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
					except BadHeaderError:
						global errormsg
						errormsg = "Invalid header found while sending email"
						return redirect('ServerError')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="app/password/password_reset.html", context={"password_reset_form":password_reset_form})

def register_request(request):
	if request.method == "POST":
		if User.objects.filter(email=request.POST['email'], is_active=True).exists():
			messages.error(request, "Email already registered.")
			return redirect("register")
		elif User.objects.filter(email=request.POST['email'], is_active=False).exists():
			user = User.objects.filter(email=request.POST['email'], is_active=False).first()
			current_site = get_current_site(request)  
			subject = 'Activation link has been sent to your email id'  
			message = render_to_string('app/password/acc_active_email.html', {  
				'user': user,  
				'domain': current_site.domain,  
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),  
				'token': account_activation_token.make_token(user),  
			})
			to_email = user.email
			send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])
			return render(request=request, template_name="app/password/acc_activation_email.html")
		else:
			form = forms.NewUserForm(request.POST)
			if form.is_valid():
				user = form.save(commit=False)
				user.is_active = False
				user.save()
				current_site = get_current_site(request)  
				subject = 'Activation link has been sent to your email id'  
				message = render_to_string('app/password/acc_active_email.html', {  
					'user': user,  
					'domain': current_site.domain,  
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),  
					'token': account_activation_token.make_token(user),  
				})
				to_email = form.cleaned_data.get('email')
				send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])
				return render(request=request, template_name="app/password/acc_activation_email.html")
			else:
				return render(request=request, template_name="app/register.html", context={"register_form":form})
	form = forms.NewUserForm()
	return render (request=request, template_name="app/register.html", context={"register_form":form})

def activate(request, uidb64, token): 
	try:  
		uid = force_str(urlsafe_base64_decode(uidb64))  
		user = User.objects.get(pk=uid)  
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
		user = None  
	if user is not None and account_activation_token.check_token(user, token):  
		user.is_active = True  
		user.save()
		return render(request,'app/password/acc_activated.html')
	else:  
		return HttpResponse('Activation link is invalid!')  

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active == True:
					login(request, user)
					obj = models.UserSubscription.objects.filter(user__username=username)
					if obj and obj[0].status:
						return redirect("home")
					else:
						return redirect("pricing")
				else:
					messages.error(request,"Your account is not active.")				
		else:
			if User.objects.filter(username=request.POST['username']).exists():
				messages.error(request,"Password is incorrect")
			else:
				messages.error(request,"Username is incorrect")
			return render(request=request, template_name="app/login.html", context={"login_form":form})
	form = AuthenticationForm()
	return render(request=request, template_name="app/login.html", context={"login_form":form})

@login_required
def logout_request(request):
    logout(request)
    return redirect("home")

def str_to_list(value):
	value = value.replace("[",'').replace("'","").replace(" ","").replace("]","")
	return value.split(",")
@method_decorator(login_required, name='dispatch')
class index(View):
	template_name = 'app/index.html'

	def get_context(self):
		context = {}
		if self.request.user.is_superuser:
			context['qs'] = models.Campaign.objects.all().order_by('-id')
		else:
			context['qs'] = models.Campaign.objects.filter(user=self.request.user).order_by('-id')
		return context

	def get(self,request):
		'''delete campaign created before 30 days'''
		models.Campaign.objects.filter(created_at__lte=timezone.now()-timedelta(days=30)).delete()

		if not models.UserSubscription.objects.filter(user=request.user).exists():
			obj = models.UserSubscription.objects.filter(user=request.user)
			if obj and obj[0].status:
				return redirect("pricing")
			return redirect("pricing")
		return render(request,self.template_name,self.get_context())
	
	def post(self,request,*args, **kwargs):
		print("-----------------Post-----------------")
		print(request.POST)
		cobj = models.Campaign.objects.create(user=request.user,Name=request.POST['Name'])
		print(cobj)
		for key in request.FILES.keys():
			print(key," key")
			if key.startswith("AdFile"):
				w,h = key.split(" ")[1].split("x")
				new = request.POST.copy()
				new['Campaign'] = cobj.id
				files = request.FILES.copy()
				files['image'] = request.FILES[key]
				form = forms.CompaignUploadForm(new,files)
				if form.is_valid():
					print("form is valid")
					uobj = form.save()
					# uobj = models.CompaignUpload.objects.create(image=request.FILES[key],campaignupload=cobj)
					# print(uobj)
					for url in request.POST.getlist(f'CampaignUrl {w}x{h}'):
						print(" i am here")
						sobj = models.Size.objects.get(weight=w,height=h,urlimage__URL__id=url)
						print(sobj)
						models.CompainUploadSize.objects.create(campaignupload=uobj,size=sobj)
				else:
					print(form.errors)
		print('Record created')
		# video = False
		# fs = FileSystemStorage()
		# files = []
		# for i in request.FILES.getlist('AdFile'):
		# 	files.append(i.name)
		# new = request.POST.copy()
		# new['AdFile'] = files
		# new['user'] = request.user
		# form = forms.CampaignForm(new)
		# if form.is_valid():
		# 	obj = form.save()
		# 	try:
		# 		if not os.path.exists(f'media/{obj.id}_ads'):
		# 			os.makedirs(f'media/{obj.id}_ads')
		# 		if not os.path.exists(f'media/{obj.id}'):
		# 			os.makedirs(f'media/{obj.id}')
		# 		for i in request.FILES.getlist('AdFile'):
		# 			fs.save(f'media/{obj.id}_ads/{i.name}', i)
		# 			if "video/" in mime.from_file(f'media/{obj.id}_ads/{i.name}'):
		# 				tasks.save_frames(f'media/{obj.id}_ads/{i.name}',f'media/{obj.id}_ads/{i.name.split(".")[0]}',request.POST['CrawlUrl'] if request.POST['CrawlUrl'] else 1)
		# 				video = True
		# 				os.remove(os.path.join(settings.BASE_DIR/"media", f'{obj.id}_ads/{i.name}'))
		# 		for i in str_to_list(request.POST['CampaignUrl']):
		# 			dt = models.ClientUrl.objects.filter(Url__contains=i,Type="Image" if not video else "Video")
		# 			for j in dt:
		# 				obj.CampaignUrl.add(j)
		# 		if kwargs['page'] == "image":
		# 			for i in str_to_list(request.POST['mobiledevices']):
		# 				obj.mobiledevices.add(i)
		# 			for i in str_to_list(request.POST['desktopdevices']):
		# 				obj.desktopdevices.add(i)
		# 		obj.save()
		# 		signals.campaig_created.send(sender=self.__class__, instance=obj, video=video)
		# 	except:
		# 		obj.delete()
		# 	return redirect('home')
		# print(form.errors)
		context = self.get_context()
		# context['errors'] = form.errors
		# return render(request,self.template_name, context)
@method_decorator(login_required, name='dispatch')
class create_campaign(View):
	template_name = 'app/create_campaign.html'

	def post(self,request):
		context = {}
		if models.Campaign.objects.filter(user=request.user,Name=request.POST['Name']).exists():
			messages.info(request,"Champaign already exists.")
			return redirect('home')
		context['Name'] = request.POST['Name']
		# name = request.POST['Name']
		# user = request.user
		# obj=models.Campaign.objects.create(
        #        user = user,
        #        Name = name
               
        #    )
		# obj.save
		return render(request,self.template_name,context)
@method_decorator(login_required, name='dispatch')
class upload_ad(View):
	template_name = 'app/upload_ad.html'

	def get(self,request):
		context = {}
		context['Name'] = request.GET['Name']
		context['CampaignUrl'] = request.GET.getlist('CampaignUrl')
		context['mobiledevices'] = request.GET['mobiledevices'].split(',')
		context['desktopdevices'] = request.GET['desktopdevices'].split(',')
		context['obj'] = models.Device.objects.filter(pk__in=request.GET['mobiledevices'].split(',')).union(models.Device.objects.filter(pk__in=request.GET['desktopdevices'].split(',')))
		context['page'] = 'image'
		return render(request,self.template_name,context)
	
	def post(self,request):
		context ={}
		context['Name'] = request.POST['Name']
		context['CampaignUrl'] = request.POST.getlist('CampaignUrl')
		context['page'] = 'video'
		return render(request,self.template_name,context)
@method_decorator(login_required, name='dispatch')
class select_sizes(View):
	template_name = 'app/select_sizes.html'
	context = {}
	def get(self,request,*args, **kwargs):
		sizes = models.Size.objects.all().distinct('weight','height')
		context = self.context
		context['query'] = sizes
		context['Name']	= kwargs['Name']	
		# context['mobiledevices'] = models.Device.objects.filter(device="Mobile").order_by('-id')
		# context['desktopdevices'] = models.Device.objects.filter(device="Desktop").order_by('-id')
		# context['video'] = False
		return render(request,self.template_name,context)

@method_decorator(login_required, name='dispatch')
class select_url(View):
	template_name = 'app/select_url.html'

	def get(self,request,*args, **kwargs):
		context = {}
		context['Name'] = kwargs['Name']
		qs1 = models.ClientUrl.objects.filter(Type = "Video").distinct('Url')
		qs1 = list(qs1.values('Url'))
		for i in qs1:
			i['Url'] = i['Url'].split("://")[1].split("/")[0].replace("www.","").replace("pk.","")
		qs1 = [dict(t) for t in {tuple(d.items()) for d in qs1}]
		qs1 = sorted(qs1, key=lambda d: d['Url'])
		context['urls'] = qs1
		context['video'] = True
		return render(request,self.template_name,context)

	def post(self,request,*args, **kwargs):
		context = {}
		context['Name'] = kwargs['Name']
		context['mobiledevices'] = str(request.POST.getlist('mobiledevices')).replace("'","").replace('[','').replace(']','').replace(" ",'')
		context['desktopdevices'] = str(request.POST.getlist('desktopdevices')).replace("'","").replace('[','').replace(']','').replace(" ",'')
		qs1 = models.ClientUrl.objects.none()
		lista = list(models.Device.objects.filter(pk__in=request.POST.getlist('mobiledevices')).values('h','w'))
		for i in lista:
			qs1 = qs1.union(models.ClientUrl.objects.filter(ads__contains=[{"h":f"{i['h']}","w":f"{i['w']}"}],Type = "Image").distinct('Url'))
		lista = list(models.Device.objects.filter(pk__in=request.POST.getlist('desktopdevices')).values('h','w'))
		for i in lista:
			qs1 = qs1.union(models.ClientUrl.objects.filter(ads__contains=[{"h":f"{i['h']}","w":f"{i['w']}"}],Type = "Image").distinct('Url'))
		qs1 = list(qs1.values('Url'))
		for i in qs1:
			i['Url'] = i['Url'].split("://")[1].split("/")[0].replace("www.","")
		qs1 = [dict(t) for t in {tuple(d.items()) for d in qs1}]
		qs1 = sorted(qs1, key=lambda d: d['Url'])
		context['urls'] = qs1
		context['video'] = False
		return render(request,self.template_name,context)

@method_decorator(login_required, name='dispatch')
class verify_sizes(View):
	def post(self,request):
		w,h=request.POST['size'].split('x')
		qs = models.Size.objects.filter(weight=w,height=h).values(pk=F('urlimage__URL__pk'),Url=F('urlimage__URL__Url'))		
		print('-------------',qs)
		obj=json.loads(json.dumps(list(qs),cls=DjangoJSONEncoder))
		
		return JsonResponse(obj, status=HTTPStatus.OK,safe=False)
@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class save_url(View):
	def post(self,request):
		new = request.POST.copy()
		new['user'] = request.user
		form = forms.ClientUrlForm(new)
		if form.is_valid():
			form.save()
		if form.errors:
			context = {}
			context['errors'] = form.errors
			return JsonResponse(context,status = 400)
		else:	
			return JsonResponse({'response':'success'},status = 200)
@method_decorator(login_required, name='dispatch')
class view_screenshots(View):
	template_name = 'app/view_screenshots.html'

	def get(self,request,*args, **kwargs):
		context = {}
		context['qs'] = models.CampaignImages.objects.filter(campaign__pk=kwargs['id']).order_by("created_at")
		context['cp'] = models.Campaign.objects.filter(pk=kwargs['id'])
		return render(request,self.template_name,context)
@method_decorator(login_required, name='dispatch')
class delete_screenshots(View):
	def get(self,request,*args, **kwargs):
		models.Campaign.objects.filter(pk=kwargs['id']).delete()
		return redirect('home')

class home(View):
	template = 'app/home.html'
	def get(self,request):
		return render(request,self.template)

class adqa(View):
	template = 'app/ad-qa.html'
	def get(self,request):
		return render(request,self.template)

class adtxtpro(View):
	template = 'app/ad-txt-pro.html'
	def get(self,request):
		return render(request,self.template)

class blogs(View):
	template = 'app/blogs.html'
	def get(self,request):
		return render(request,self.template)

class aboutus(View):
	template = 'app/aboutus.html'
	def get(self,request):
		return render(request,self.template)

class pricing(View):
	template = 'app/pricing.html'
	def get(self,request):
		context = {}
		context['prices'] = models.Subscription_plan.objects.all() 
		return render(request,self.template,context)

class reviews(View):
	template = 'app/reviews.html'
	def get(self,request):
		return render(request,self.template)

class contactus(View):
	template = 'app/contactus.html'
	context={}
	def get(self,request):
		return render(request,self.template)
	
	def post(self,request):
		form = forms.ContactForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,"Message submitted successfully! Thanks for contacting.")
			return redirect('contactus')
		context = self.context
		context['form'] = form.errors
		return render(request=request, template_name=self.template,context=context)

class screenshot(View):
	template = 'app/screenshot.html'
	def get(self,request):
		return render(request,self.template)

class success(View):
	def get(self,request):
		session_id = request.GET['session_id']
		session_checkout = stripe.checkout.Session.retrieve(session_id)
		obj = models.Subscription_plan.objects.get(lookup_key=session_checkout['metadata']['lookup_key'])
		models.UserSubscription.objects.get_or_create(
			user=request.user,
			session_id=session_id,
			customer = session_checkout['customer'],
			amount_total = int(session_checkout['amount_total'])/100,
			plan = obj,
			subscription = session_checkout['subscription'],
			payment_status = session_checkout['payment_status'],
			started_at = timezone.now(),
			end_at = timezone.now() + timedelta(days=int(obj.duration)*30)
			)
		subject = 'Thank for Purchasing Subscription'  
		message = render_to_string('app/password/sub_purchased_email.txt', {  
			'user': request.user, 
		})
		to_email = request.user.email
		send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])
		return redirect('home')
		# return render(request,self.template,{'session_id':session_id})

class cancel(View):
	template = 'app/cancel.html'
	def get(self,request):
		return render(request,self.template)

class create_checkout_session(View):
	def post(self,request):
		if request.user.is_authenticated:
			obj = models.UserSubscription.objects.filter(user=request.user)
			if obj and obj[0].status:
				return redirect('home')
		prices = stripe.Price.list(
			lookup_keys=[request.POST['lookup_key']],
			expand=['data.product']
		)
		checkout_session = stripe.checkout.Session.create(
			line_items=[
				{
					'price': prices.data[0].id,
					'quantity': 1,
				},
			],
			metadata={
				"lookup_key": request.POST['lookup_key']
			},
			customer_email=request.user.email,
			mode='subscription',
			success_url=domain + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain + '/cancel',
		)
		return redirect(checkout_session.url, code=303)

class customer_portal(View):
	def get(self,request):	
		obj = models.UserSubscription.objects.filter(user=request.user).last()
		try:
			checkout_session = stripe.checkout.Session.retrieve(obj.session_id)
		except:
			global errormsg
			errormsg = "Ops! Invalid session id found! Please try again with correct details. Thank you."
			return redirect('ServerError')
			# return redirect('ServerError',message="session id doesn't exists")
		# This is the URL to which the customer will be redirected after they are
		# done managing their billing with the portal.
		return_url = f'{domain}/home/'
		portalSession = stripe.billing_portal.Session.create(
			customer=checkout_session.customer,
			return_url=return_url,
		)
		return redirect(portalSession.url, code=303)
	def post(self,request):
		# For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
		# Typically this is stored alongside the authenticated user in your database.
		checkout_session_id = request.POST.get('session_id')
		checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

		# This is the URL to which the customer will be redirected after they are
		# done managing their billing with the portal.
		return_url = f'{domain}/home/'

		portalSession = stripe.billing_portal.Session.create(
			customer=checkout_session.customer,
			return_url=return_url,
		)
		return redirect(portalSession.url, code=303)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
class webhook_received(View):
	def post(self,request):
		# Replace this endpoint secret with your endpoint's unique secret
		# If you are testing with the CLI, find the secret by running 'stripe listen'
		# If you are using an endpoint defined with the API or dashboard, look in your webhook settings
		# at https://dashboard.stripe.com/webhooks
		webhook_secret = settings.webhook_key
		request_data = json.loads(request.body)

		if webhook_secret:
			# Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
			signature = request.headers.get('stripe-signature')
			try:
				event = stripe.Webhook.construct_event(
					payload=request.body, sig_header=signature, secret=webhook_secret)
				data = event['data']
			except Exception as e:
				return e
			# Get the type of webhook event sent - used to check the status of PaymentIntents.
			event_type = event['type']
		else:
			data = request_data['data']
			event_type = request_data['type']
		data_object = data['object']

		print('event ' + event_type)
		if event['type'] == 'customer.subscription.created':
			subscription = event['data']['object']
			print('created')
		elif event['type'] == 'customer.subscription.deleted':
			subscription = event['data']['object']
			models.UserSubscription.objects.filter(subscription=subscription['id']).update(status=False,payment_status="deleted")
			print('deleted')
		elif event['type'] == 'customer.subscription.updated':
			subscription = event['data']['object']
			obj = models.UserSubscription.objects.filter(subscription=subscription['id']).exists()
			if obj:
				if subscription['cancel_at_period_end']:
					models.UserSubscription.objects.filter(subscription=subscription['id']).update(status=False,payment_status="canceled")
				else:
					models.UserSubscription.objects.filter(subscription=subscription['id']).update(status=True,payment_status="renew")
			print('updated')
		elif event['type'] == 'price.created':
			price = event['data']['object']
			product = stripe.Product.retrieve(f"{price['product']}")
			models.Subscription_plan.objects.get_or_create(stripe_price_id=price['id'],defaults={
				'Name':product['name'],
				'price':float(price['unit_amount'])/100,
				'lookup_key':price['lookup_key'],
				'duration':int(price['recurring']['interval_count']),
				'stripe_product_id':price['product']
			})
		elif event['type'] == 'price.deleted':
			price = event['data']['object']
			product = stripe.Product.retrieve(f"{price['product']}")
			models.Subscription_plan.objects.filter(stripe_price_id=price['id']).delete()
		elif event['type'] == 'price.updated':
			price = event['data']['object']
			product = stripe.Product.retrieve(f"{price['product']}")
			models.Subscription_plan.objects.update_or_create(stripe_price_id=price['id'],defaults={
				'Name':product['name'],
				'price':float(price['unit_amount'])/100,
				'lookup_key':price['lookup_key'],
				'duration':int(price['recurring']['interval_count']),
				'stripe_product_id':price['product']
			})
		else:
			print('Unhandled event type {}'.format(event['type']))

		return JsonResponse({'status': 'success'})


def selenium_view(request):
	global driver,flag,url_image_id

	category_name ='PET'
	sites=['https://doggies.com/']

	
	for site in sites:
		try:
			driver.get(site)
			print("page loadded")
			instance = models.ClientUrl.objects.create(category=category_name,Url=site)
			instance.save()
			site_id = instance.id
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
					height= style.get_attribute("height")
					width= style.get_attribute("width")
					print(width)
				
					print(style.get_attribute("style"))
					if width !='' and width != 0 and height != 0:
						content = driver.find_element(By.ID, a)
						driver = content._parent
						driver.execute_script("arguments[0].scrollIntoView(true);", content);
						highlight(content, 5, 'red', 2)
						img = Image.open('screenshot.png')
						rimg = img.copy()
						name=site[8:-1]
						making_name = name+'pic'+'_'+str(flag)
						flag = flag+1
						saved_name=making_name+'.png'
						rimg.save(f"media/screenshots/{saved_name}")
					print("-------------------------------")
				elif "aswift" in iframe:
					print("-------------------------------")
					print(style)
					a = style.get_attribute("name")
					result.append(a)
					print(style.get_attribute("name"))
					height= style.get_attribute("height")
					width=style.get_attribute("width")
					print(style.get_attribute("style"))
					print(height)
					print(width)
					if width !='' and width != 0 and height != 0:
						content = driver.find_element(By.ID, a)
						driver = content._parent
						driver.execute_script("arguments[0].scrollIntoView(true);", content);
						highlight(content, 5, 'red', 3)
						img = Image.open('screenshot.png')
						rimg = img.copy()
						name=site[8:-1]
						making_name = name+'pic'+'_'+str(flag)
						flag = flag+1
						saved_name=making_name+'.png'
						rimg.save(f"media/screenshots/{saved_name}")
						saved_path=f"media/screenshots/{saved_name}"
						site_object = models.ClientUrl.objects.get(id=site_id)
						instance = models.UrlImage.objects.create(URL=site_object, image=saved_path)
						instance.save()
						url_image_id= instance.id
						                         
						
					print("-------------------------------")
				else:
					print('no add found')



			

			def opencv_handler(img,site):
				# Read input image
				site_url=site
				get_image = img
				img = cv2.imread(img)
			

				# Gel all pixels in the image - where BGR = (34, 33, 33), OpenCV colors order is BGR not RGB
				gray = np.all(img == (0, 0, 255), 2)  # gray is a logical matrix with True where BGR = (34, 33, 33).

				# Convert logical matrix to uint8
				gray = gray.astype(np.uint8)*255

				# Find contours
				cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # Use index [-2] to be compatible to OpenCV 3 and 4
				try:
					# Get contour with maximum area
					c = max(cnts, key=cv2.contourArea)

					x, y, w, h = cv2.boundingRect(c)
					print(site_url,get_image[20:]+'=',x,y,w,h)
					site_object = models.UrlImage.objects.get(id=url_image_id)
					instance = models.Size.objects.create(urlimage=site_object, x=x,y=y,height=h,weight=w)
					instance.save()

				except ValueError as ve:
					print('Dimention Error')

				
				
				

           
			screenshots =glob.glob("media/screenshots*/*.png")
			print(screenshots) 


			for image in screenshots:
				if site[8:-1] in image:
					opencv_handler(image,site)
		

		except WebDriverException:
			print("page down")
		return HttpResponse("site scraped!")



def ImagePlace(request):
	
	# Read input image
	img = cv2.imread(img)
	img2 = cv2.imread('image.png')

	# Gel all pixels in the image - where BGR = (34, 33, 33), OpenCV colors order is BGR not RGB
	gray = np.all(img == (0, 0, 255), 2)  # gray is a logical matrix with True where BGR = (34, 33, 33).

	# Convert logical matrix to uint8
	gray = gray.astype(np.uint8)*255

	# Find contours
	cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # Use index [-2] to be compatible to OpenCV 3 and 4

	# Get contour with maximum area
	c = max(cnts, key=cv2.contourArea)

	x, y, w, h = cv2.boundingRect(c)
	print(x,y,w,h)
	# Draw green rectangle for testing
	# cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), thickness = 2)
	resized_down = cv2.resize(img2, (w,h), interpolation= cv2.INTER_LINEAR)
	cv2.imwrite('resize.png', resized_down)
	# Show result
	resize_image = cv2.imread('resize.png')
	img[y:y+h,x:x+w]=resize_image
	random_name = ''.join(random.choices(string.ascii_uppercase +
							string.digits, k=7))
	saved_name='./results'+'/'+random_name+'.png'
	cv2.imwrite(saved_name, img)
	


	# screenshots =glob.glob("scraped_images*/*.png") 


	# for image in screenshots:
	# 	opencv_handler(image)
	# files = glob.glob('scraped_images/*')
	return HttpResponse("done")



@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class select_url(View):
	def post(self,request):
		new = request.POST
		print(new)
		# new['user'] = request.user
		# form = forms.ClientUrlForm(new)
		# if form.is_valid():
		# 	form.save()
		# if form.errors:
		# 	context = {}
		# 	context['errors'] = form.errors
		# 	return JsonResponse(context,status = 400)
		# else:	
		return JsonResponse({'response':'success'},status = 200)
from http import HTTPStatus
import json
from django.http import JsonResponse
from django.views import View
from django.shortcuts import redirect, render
from adstool import models
import os
from adstool import forms
from adstool import modules
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.

if not os.path.exists(f"media/templates"):
    os.makedirs(f"media/templates")
if not os.path.exists(f"media/ads"):
    os.makedirs(f"media/ads")
if not os.path.exists(f"media/ads/assets"):
    os.makedirs(f"media/ads/assets")
@method_decorator(login_required, name='dispatch')
class index(View):
    template = "adstool/index.html"
    context = {}
    def get(self,request):
        context = self.context
        context['templates'] = models.Template.objects.all().order_by('-id')
        context['ads'] = models.Ads.objects.filter(user=request.user).order_by('-id')
        return render(request=request, template_name=self.template, context=context)

class AdsView(View):
    template = "adstool/AdsView.html"
    context = {}
    def get(self,request,*args, **kwargs):
        context = self.context
        context['ad'] = models.Ads.objects.get(pk=kwargs['id'])
        context['FontCategory'] = models.FontCategory.objects.all().order_by('category')
        return render(request=request, template_name=self.template, context=context)
class GetFonts(View):
    def get(self,request,*args, **kwargs):
        obj = models.FontFamily.objects.filter(category__id=kwargs['id']).values('family','files')
        obj = json.loads(json.dumps(list(obj), cls=DjangoJSONEncoder))
        return JsonResponse(obj,safe=False,status = HTTPStatus.OK)
class TemplateView(View):
    template = "adstool/TemplateView.html"
    context = {}
    def get(self,request,*args, **kwargs):
        context = self.context
        context['Template'] = models.Template.objects.get(pk=kwargs['id'])
        return render(request=request, template_name=self.template, context=context)

class Ads(View):
    template = "adstool/ads.html"
    context = {}
    
    def get(self,request,*args, **kwargs):
        context = self.context
        context['ad'] = kwargs['id']
        return render(request=request, template_name=self.template, context=context)
    
    def post(self,request,*args, **kwargs):
        new = request.POST.copy()
        new['template'] = kwargs['id']
        new['user'] = request.user
        new['info'] = models.Template.objects.get(id=kwargs['id']).info
        form = forms.AdsForm(new)
        if form.is_valid():
            obj = form.save()
            
            return redirect(f"/adstool/AdsView/{obj.id}/")
        print(form.errors)
        context = self.context
        context['ads'] = request.POST['template']
        return render(request=request, template_name=self.template, context=context)

class UpdateAds(View):
    def post(self,request,*args, **kwargs):
        obj = models.Ads.objects.get(pk=kwargs['id'])
        print(request.POST)
        if "logo" in request.FILES.keys():
            fs = FileSystemStorage()
            fs.save(f'media/ads/assets/{request.FILES["logo"].name}', request.FILES['logo'])
            print(obj.logo.name)
            if not obj.logo.name == "ads/logo.png":
                obj.logo.delete(save=False)
            obj.logo.save("{}".format({request.FILES['logo'].name}), File(open(f"media/ads/assets/{request.FILES['logo'].name}", "rb")))
            obj.save()
            os.remove(f'media/ads/assets/{request.FILES["logo"].name}')
        elif "product" in request.FILES.keys():
            print('product')
            fs = FileSystemStorage()
            fs.save(f'media/ads/assets/{request.FILES["product"].name}', request.FILES['product'])
            if not obj.product.name == "ads/product.png":
                obj.product.delete(save=False)
            obj.product.save("{}".format({request.FILES['product'].name}), File(open(f"media/ads/assets/{request.FILES['product'].name}", "rb")))
            obj.save()
            os.remove(f'media/ads/assets/{request.FILES["product"].name}')
        else:
            for i in request.POST.keys():
                if i in obj.info['ad']:
                    obj.info['ad'][i] = request.POST[i]
                elif i == "ctatext":
                    obj.info['ad']['cta']['text'] = request.POST[i]
                elif i == "ctafamily":
                    obj.info['ad']['cta']['family'] = request.POST[i]
                elif i == "ctastyle":
                    obj.info['ad']['cta']['style'] = request.POST[i]
                elif i == "ctasize":
                    obj.info['ad']['cta']['size'] = int(request.POST[i])
                elif i == "ctacolor":
                    obj.info['ad']['cta']['color'] = request.POST[i]
                
                elif i == "subheadtext":
                    obj.info['ad']['subhead']['text'] = request.POST[i]
                elif i == "subheadfamily":
                    obj.info['ad']['subhead']['family'] = request.POST[i]
                elif i == "subheadstyle":
                    obj.info['ad']['subhead']['style'] = request.POST[i]
                elif i == "subheadsize":
                    obj.info['ad']['subhead']['size'] = int(request.POST[i])
                elif i == "subheadcolor":
                    obj.info['ad']['subhead']['color'] = request.POST[i]
                
                elif i == "headlinetext":
                    obj.info['ad']['headline']['text'] = request.POST[i]
                elif i == "headlinefamily":
                    obj.info['ad']['headline']['family'] = request.POST[i]
                elif i == "headlinestyle":
                    obj.info['ad']['headline']['style'] = request.POST[i]
                elif i == "headlinesize":
                    obj.info['ad']['headline']['size'] = int(request.POST[i])
                elif i == "headlinecolor":
                    obj.info['ad']['headline']['color'] = request.POST[i]
        obj.save()
        modules.update_ads(obj)
        return JsonResponse({"status":"success"})
from django.urls import path
from adstool import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',views.index.as_view(),name='index'),
    path('TemplateView/<int:id>/',views.TemplateView.as_view(),name='TemplateView'),
    path('AdsView/<int:id>/',views.AdsView.as_view(),name='AdsView'),
    path('Ads/<int:id>/',views.Ads.as_view(),name='Ads'),
    path('UpdateAds/<int:id>/',views.UpdateAds.as_view(),name='UpdateAds'),
    path('GetFonts/<int:id>/',views.GetFonts.as_view(),name='GetFonts'),
]
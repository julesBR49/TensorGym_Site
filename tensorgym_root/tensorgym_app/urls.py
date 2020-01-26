from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='tensorgym_home'),
    path('about/', views.about, name='tensorgym_about'),
]
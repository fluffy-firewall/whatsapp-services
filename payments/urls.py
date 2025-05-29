from django.urls import path
from . import views

urlpatterns = [
    path('webhook/yoco/', views.yoco_webhook, name='yoco_webhook'),
]
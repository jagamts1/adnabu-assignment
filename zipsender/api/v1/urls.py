from django.urls import path
from zipsender.api.v1 import views

urlpatterns = [
    path('mail/', views.ZipSender.as_view()),
]

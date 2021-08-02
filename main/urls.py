from django import urls
from main.models import *
from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from main.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('customer/', create_customer),
    path('customer/<int:pk>', customer_detail),
    path('message/', create_message),
    path('customer/<int:pk>', message_detail),
    path('group/', create_group),
    path('customer/<int:pk>', group_detail),
    path('transaction/', create_transaction),
    path('customer/<int:pk>', transaction_detail),
    path('sender/', create_sender),
    path('customer/<int:pk>', sender_detail),
    path('template/', create_template),
    path('customer/<int:pk>', template_detail),
    path('contact/', create_contact),
    path('customer/<int:pk>', contact_detail),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

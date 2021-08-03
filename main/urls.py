from django import urls
from main.models import *
from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from main.views import *
from django.conf.urls import url
from allauth.account.views import confirm_email
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # path('user/', create_user),
    url('rest-auth/', include('rest_auth.urls')),
    url('rest-auth/registration/', include('rest_auth.registration.urls')),
    url('account/', include('allauth.urls')),
    url('accounts-rest/registration/account-confirm-email/(?P<key>.+)/$',
        confirm_email, name='account_confirm_email'),

    path('user/<int:pk>', user_detail),
    path('message/', create_message),
    path('user/<int:pk>', message_detail),
    path('group/', create_group),
    path('user/<int:pk>', group_detail),
    path('transaction/', create_transaction),
    path('user/<int:pk>', transaction_detail),
    path('sender/', create_sender),
    path('user/<int:pk>', sender_detail),
    path('template/', create_template),
    path('user/<int:pk>', template_detail),
    path('contact/', create_contact),
    path('user/<int:pk>', contact_detail),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

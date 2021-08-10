from main.views import *
from django.urls import path


urlpatterns = [

    path('message/', create_message),
    path('user/<int:pk>', message_detail),
    path('group/', create_group),
    path('group/<int:pk>', group_detail),
    path('transaction/', create_transaction),
    path('user/<int:pk>', transaction_detail),
    path('sender/', create_sender),
    path('sender/<int:pk>', sender_detail),
    path('template/', create_template),
    path('user/<int:pk>', template_detail),
    path('contact/', create_contact),
    path('user/<int:pk>', contact_detail),
]

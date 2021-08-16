from django.urls import path

from main.views import *

urlpatterns = [

    path('message/', create_message),
    path('message/<int:pk>', message_detail),
    path('group/', create_group),
    path('group/<int:pk>', group_detail),
    path('sender/', create_sender),
    path('sender/<int:pk>', sender_detail),
    path('template/', create_template),
    path('template/<int:pk>', template_detail),
    path('contact/', create_contact),
    path('contacts/', create_contacts),
    path('contact/<int:pk>', contact_detail),
    path('creditcard/', view_credit_card_details),
    path('creditcard/<int:pk>', creditCard_detail),
    path('transaction/', view_transaction),
    path('verifyPayments/', verify_payment)
]

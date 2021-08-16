from main.views import *
from django.urls import path


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
    path('contact/<int:pk>', contact_detail),
    path('creditcard/', view_credit_card_details),
    path('creditcard/<int:pk>', delete_creditCard),
    path('transaction/<int:pk>', view_one_transaction),
    path('transaction/', view_all_transaction),
    path('verifyPayments/', verify_payment),
    path('account_balance/', account_balance)
]

from django.db.models import fields
from rest_framework import serializers
from main.models import *
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


admin.site.register(Contact)
admin.site.register(User)
admin.site.register(Message)
admin.site.register(PaymentTransaction)
admin.site.register(Balance)
admin.site.register(Payment_verification)
admin.site.register(Credit_card_details)
admin.site.register(Group)
admin.site.register(Template)
admin.site.register(Sender)

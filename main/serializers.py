from django.contrib.auth import get_user_model
from django.db import models
from django.utils import translation
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.fields import EmailField
from rest_framework.serializers import ModelSerializer

from main.models import *

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__'


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['content', 'sender_name']


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class GroupSerializer(ModelSerializer):
    contacts = ContactSerializer(many=True,read_only=True)

    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = ('id',)
    


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'


class SenderSerializer(ModelSerializer):
    class Meta:
        model = Sender
        fields = '__all__'


class TemplateSerializer(ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'


class PaymentVerificationSerializer(ModelSerializer):
    class Meta:
        model = Payment_verification
        fields = '__all__'

class PaymentTransactionSerializer(ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'


class CreditCardDetailsSerializer(ModelSerializer):
    class Meta:
        model = Credit_card_details
        fields = '__all__'


class Account_balanceSerializer(ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'

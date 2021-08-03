from django.db import models
from django.utils import translation
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from main.models import *


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name',
                  'last_name', 'phone_no', 'joined_date']


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class SenderSerializer(ModelSerializer):
    class Meta:
        model = Sender
        fields = '__all__'


class TemplateSerializer(ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

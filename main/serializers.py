from django.db import models
from django.utils import translation
from rest_framework.fields import EmailField
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from main.models import *
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__'


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['content', 'sender_name']


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


class ContactInitSerializer(ModelSerializer):
    class Meta:
        model = ContactInit
        fields = '__all__'

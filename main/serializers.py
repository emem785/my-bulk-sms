from djoser.email import ActivationEmail
from django.db import models
from django.utils import translation
from rest_framework.fields import EmailField
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from main.models import *
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__'


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name',
                  'last_name', 'phone_no', 'username', 'password']

    def save(self, request):
        user = User(
            email=request.data['email'],
            username=request.data['username'],
            phone_no=request.data['phone_no'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
        )
        user.set_password(request.data['password'])
        user.save()
        return user


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

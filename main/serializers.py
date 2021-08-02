from django.db import models
from django.utils import translation
from rest_framework.serializers import ModelSerializer
from main.models import *


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


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

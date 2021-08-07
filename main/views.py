import json

import requests
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_400_BAD_REQUEST,
                                   HTTP_405_METHOD_NOT_ALLOWED)
from whisper.settings import logger

from .models import *
from .serializers import *


def test_view(request):
        return render(request, "redirect.html")

def activate_email(request):

    if request.method == "GET":
        uid = request.GET.get('uid')
        token = request.GET.get('token')
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/auth/users/activation/"
        post_data = {'uid': uid, 'token': token}
        result = requests.post(post_url, json=post_data, headers={
                               "content-type": "application/json"})
        logger.log(msg=result.text, level=50)

        return render(request, "redirect.html")



def reset_password(request):

    if request.method == "GET":
        uid = request.GET.get('uid')
        token = request.GET.get('token')
        context = {"uid": uid, "token": token}
        return render(request, "reset_password.html", context=context)

    password = request.POST.get('password')
    uid = request.POST.get('uid')
    token = request.POST.get('token')
    protocol = 'https://' if request.is_secure() else 'http://'
    web_url = protocol + request.get_host()
    post_url = web_url + "/auth/users/reset_password_confirm/"
    post_data = {'uid': uid, 'token': token, 'new_password': password}
    print(post_data)
    result = requests.post(post_url, json=post_data, headers={
                               "content-type": "application/json"})

    return JsonResponse({"msg": "success"})


@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated,))
def create_message(request):
    if request.method == 'POST':

        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            # useremail = serializer.validated_data.get('email')
            # message_queryset = Message.objects.filter(email=useremail)

            # if message_queryset.exists():
            # message = {
            #     "status": "Sorry email already exist, please try another email"
            # }
            #     print("[[[[[[[[[[[[[[[[[[[[[")
            #     print('..................')
            #     print(message)
            # message = {
            #     "status": "Sorry email already exist, please try another email"
            # }

            serializer.save()
            message = {
                "status": "Message Sent"
            }
            print("[[[[[[[[[[[[[[[[[[[[[")
            print('..................')
            print(message)

            return Response(data=message, status=HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

# TODO here is the code I was talking about
    elif request.method == 'GET':
        header = request.headers['Authorization']
        token = header.split(" ")[1]
        user = Token.objects.get(key=token).user
        message = Message.objects.filter(user=user)
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def message_detail(request, pk, format=None):

    try:
        message = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_group(request):
    if request.method == 'POST':

        serializer = GroupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            message = {
                "status": "Success"
            }
            print("[[[[[[[[[[[[[[[[[[[[[")
            print('..................')
            print(message)

            return Response(data=message, status=HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    # elif request.method == 'GET':
    #     customer = Customer.objects.all()
    #     serializer = CustomerSerializer(customer, many=True)
    #     return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def group_detail(request, pk, format=None):

    try:
        group = Group.objects.get(pk=pk)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_sender(request):
    if request.method == 'POST':

        serializer = SenderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            message = {
                "status": "Success"
            }
            print("[[[[[[[[[[[[[[[[[[[[[")
            print('..................')
            print(message)

            return Response(data=message, status=HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    # elif request.method == 'GET':
    #     customer = Customer.objects.all()
    #     serializer = CustomerSerializer(customer, many=True)
    #     return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def sender_detail(request, pk, format=None):

    try:
        sender = Sender.objects.get(pk=pk)
    except Sender.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SenderSerializer(sender)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CustomerSerializer(sender, data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        sender.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_contact(request):
    if request.method == 'POST':
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            message = {
                "status": "Success"
            }
            print("[[[[[[[[[[[[[[[[[[[[[")
            print('..................')
            print(message)

            return Response(data=message, status=HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    # elif request.method == 'GET':
    #     customer = Customer.objects.all()
    #     serializer = CustomerSerializer(customer, many=True)
    #     return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def contact_detail(request, pk, format=None):

    try:
        contact = Contact.objects.get(pk=pk)
    except Contact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GroupSerializer(contact, data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_template(request):
    if request.method == 'POST':
        serializer = TemplateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            message = {
                "status": "Success"
            }
            print("[[[[[[[[[[[[[[[[[[[[[")
            print('..................')
            print(message)

            return Response(data=message, status=HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    # elif request.method == 'GET':
    #     customer = Customer.objects.all()
    #     serializer = CustomerSerializer(customer, many=True)
    #     return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def template_detail(request, pk, format=None):

    try:
        template = Template.objects.get(pk=pk)
    except Template.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TemplateSerializer(template)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TemplateSerializer(template, data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_transaction(request):
    if request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            message = {
                "status": "Success"
            }
            print("[[[[[[[[[[[[[[[[[[[[[")
            print('..................')
            print(message)

            return Response(data=message, status=HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    # elif request.method == 'GET':
    #     customer = Customer.objects.all()
    #     serializer = CustomerSerializer(customer, many=True)
    #     return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def transaction_detail(request, pk, format=None):

    try:
        transaction = Transaction.objects.get(pk=pk)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GroupSerializer(transaction)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

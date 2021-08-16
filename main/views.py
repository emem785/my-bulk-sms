import json
from functools import partial
from re import template

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

from main.helpers.helper_functions import *

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

    return render(request, "redirect.html")


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
        user = user_token_extractor(request, Token)

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


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def create_group(request):
    if request.method == 'POST':

        user = user_token_extractor(request, Token)
        serializer = GroupSerializer(data=request.data)
        serializer.initial_data["user"] = user.email

        if serializer.is_valid():
            serializer.save()
            user = user_token_extractor(request, Token)
            group = Group.objects.filter(user=user.email)
            serializer = GroupSerializer(group, many=True)
            return Response(data=serializer.data, status=HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        user = user_token_extractor(request, Token)
        group = Group.objects.filter(user=user.email)
        serializer = GroupSerializer(group, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def group_detail(request, pk, format=None):

    user = user_token_extractor(request, Token)
    try:
        group = Group.objects.get(pk=pk, user=user)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        contacts = Contact.objects.filter(group=group)
        serializer = ContactSerializer(contacts,many=True)
        return Response(serializer.data, status=200)


    elif request.method == 'PUT':
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        group.delete()
        user = user_token_extractor(request, Token)
        group = Group.objects.filter(user=user.email)
        serializer = GroupSerializer(group, many=True)
        return Response(serializer.data)


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def create_sender(request):
    if request.method == 'POST':
        userid = {
            "user": str(user_token_extractor(request, Token))
        }
        print("<<<<<<<<<>>>>>>>>>>>>>>>")
        print(userid)

        user_request = request.data
        print("<<<<<<<<<>>>>>>>>>>>>>>>")
        print(user_request)

        users_request = {**user_request, **userid}
        print("<<<<<<<<<>>>>>>>>>>>>>>>")
        print(users_request)
        serializer = SenderSerializer(data=users_request)
        print("<<<<<<<<<>>>>>>>>>>>>>>>")
        print(serializer)

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

    elif request.method == 'GET':
        user = user_token_extractor(request, Token)

        sender = Sender.objects.filter(user=user)
        serializer = SenderSerializer(sender, many=True)
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def sender_detail(request, pk, format=None):

    user = user_token_extractor(request, Token)
    try:
        sender = Sender.objects.get(pk=pk, user=user)
    except Sender.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SenderSerializer(sender)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SenderSerializer(sender, data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        sender.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_contacts(request):
    if request.method == 'POST':
        serializer = ContactSerializer(data=request.data,many=True)

        if serializer.is_valid():
            serializer.save()
            message = {"msg":"success"}
            return Response(message, status=HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST','GET','DELETE'])
@permission_classes((IsAuthenticated,))
def create_contact(request):
    if request.method == 'POST':
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            contacts = Contact.objects.filter(group=int(request.data["group"]))
            serializer = ContactSerializer(contacts, many=True)
            return Response(serializer.data, status=HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        delete_ids = request.data["contacts"]
        contacts = Contact.objects.filter(pk__in=delete_ids).delete()
        contacts = Contact.objects.filter(group=int(request.data["group"]))
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data, status=HTTP_201_CREATED)




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
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated,))
def create_template(request):
    if request.method == 'POST':
        userid = {
            "user": str(user_token_extractor(request, Token))
        }
        print("<<<<<<<<<>>>>>>>>>>>>>>>")
        print(userid)

        user_request = request.data
        print("<<<<<<<<<>>>>>>>>>>>>>>>")
        print(user_request)

        users_request = {**user_request, **userid}
        print("<<<<<<<<<>>>>>>>>>>>>>>>")
        print(users_request)
        serializer = TemplateSerializer(data=users_request)
        print("<<<<<<<<<>>>>>>>>>>>>>>>")
        print(serializer)

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
    elif request.method == 'GET':
        user = user_token_extractor(request, Token)

        template = Template.objects.filter(user=user)
        serializer = TemplateSerializer(template, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def template_detail(request, pk, format=None):

    user = user_token_extractor(request, Token)

    try:
        template = Template.objects.get(pk=pk, user=user)
    except Template.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TemplateSerializer(template)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TemplateSerializer(template, data=request.data,partial=True)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def view_all_transaction(request):
    if request.method == 'GET':
        user = user_token_extractor(request, Token)

        transaction = PaymentTransaction.objects.filter(user=user)
        serializer = PaymentTransactionSerializer(transaction, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def view_one_transaction(request, pk, format=None):
    user = user_token_extractor(request, Token)
    try:
        transaction = PaymentTransaction.objects.filter(pk=pk, user=user)
    except PaymentTransaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PaymentTransactionSerializer(transaction, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def view_credit_card_details(request):
    if request.method == 'GET':
        user = user_token_extractor(request, Token)

        credit_card_detail = Credit_card_details.objects.filter(user=user)
        serializer = CreditCardDetailsSerializer(credit_card_detail, many=True)
        return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_creditCard(request, pk, format=None):

    user = user_token_extractor(request, Token)

    try:
        creditCardDetail = Credit_card_details.objects.get(pk=pk, user=user)
    except Credit_card_details.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        creditCardDetail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def verify_payment(request):
    if request.method == 'POST':
        userid = {
            "user": str(user_token_extractor(request, Token))
        }
        print("<<<<<<<<<>>>>>>>>>>>>>>>")
        print(userid)

        user_request = request.data
        print("<<<<<<<<<>>>>>>>>>>>>>>>")
        print(user_request)

        users_request = {**user_request, **userid}
        print("<<<<<<<<<>>>>>>>>>>>>>>>")
        print(users_request)
        serializer = PaymentVerificationSerializer(data=users_request)
        print("<<<<<<<<<>>>>>>>>>>>>>>>")
        print(serializer)

        if serializer.is_valid():
            serializer.save()
            user = users_request.get('user')
            user_ref = user_request.get('user_ref')
            reason = user_request.get('reason')
            savecard = user_request.get('save_card')
            response = Payment_verification.paystack_request(
                user, user_ref, reason, savecard)

            print("[[[[[[[[[[[[[[[[[[[[[")
            print('..................')
            print(response)

            return Response(data=response, status=HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def account_balance(request):
    if request.method == 'GET':
        user = user_token_extractor(request, Token)

        balance = Account_balanceSerializer.objects.filter(user=user)
        serializer = Account_balanceSerializer(balance, many=True)
        return Response(serializer.data)

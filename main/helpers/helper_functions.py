import requests

# import pandas as pd
# from functools import Iru_cache

# from requests.api import head

# # def customerRegistration():


def user_token_extractor(request, Token):
    header = request.headers['Authorization']
    token = header.split(" ")[1]
    user = Token.objects.get(key=token).user
    print("//////////////////", "CHECKING")
    print(user)

    return user


def paystack_payment_request(user_ref):
    base_url = f'https://api.paystack.co/transaction/verify/{user_ref}'
    authorization = "Bearer sk_test_42aad857a6cea5f78ed631260a1f75faafa930ae"
    headers = {
        'AUTHORIZATION': authorization
    }
    response = requests.get(base_url, headers=headers)
    data = response.json()
    print('>>>>>>paystack direct response>>>>>>>>>>>>>>>')
    print(data)
    return data


def unit_converter(amount):
    unit = float(amount) / 2.75
    return float(unit)


def initial_bonus_sum(amount):
    amount = float(amount) + 20.75
    return str(amount)

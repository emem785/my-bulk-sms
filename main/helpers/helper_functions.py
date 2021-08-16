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
    authorization = "Bearer sk_test_e6afc1fee39acefe9f16fa769cd5eaf62db7c21b"
    headers = {
        'AUTHORIZATION': authorization
    }
    response = requests.get(base_url, headers=headers)
    data = response.json()
    print('>>>>>>paystack direct response>>>>>>>>>>>>>>>')
    print(data)
    return data


def unit_converter(amount):
    unit = float(amount) / 2.50
    return float(unit)


def initial_bonus_sum(amount):
    amount = float(amount) + 1000.00
    return str(amount)

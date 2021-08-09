# import requests
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

        
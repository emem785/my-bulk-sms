from itertools import islice
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


def contact_element_extractor(request, userid):
    group_name = {
        "group": request.get('group')
    }
    print("<<<<<<<<<>>>>>>>>>>>>>>>")
    print(group_name)

    obj = {**group_name, **userid}
    print("<<<<<<<<<>>>>>>>>>>>>>>>")
    print(obj)

    if not request.get('first_name') == None:
        first_name = {
            "first_name": request.get('first_name')
        }
        obj = {**obj, **first_name}
        print("<<<<<<<<<>>>>>>>>>>>>>>>")
        print(obj)

    if not request.get('last_name') == None:
        last_name = {
            "last_name": request.get('last_name')
        }
        obj = {**obj, **last_name}
        print("<<<<<<<<<>>>>>>>>>>>>>>>")
        print(obj)

    print("contact_element_extractor")
    print(obj)

    return obj


def contact_row_generator(user_request_object, contact):

    contact_obj = {

        "mobile_numbers": contact
    }

    contact_row = {**user_request_object, **contact_obj}

    print('.........contact generator............')
    print(contact_row)

    return contact_row

# def contact_batch_insert(contactsList, contactModel, user_request_obj):
#     batch_size = len(contactsList)

#     def contact_row_generator(user_request_object, contact):

#         contact_obj = {

#             "mobile_numbers": contact
#         }

#         contact_row = {**user_request_object, **contact_obj}

#         print('.........contact generator............')
#         print(contact_row)

#         return contact_row

#     objs = contactModel.objects.bulk_create([contact_row_generator(
#         user_request_obj, contact) for contact in contactsList])
#     return objs

    # while True:
    #     batch = list(islice(contact_obj_list, batch_size))
    #     if not batch:
    #         break
    #     contactModel.objects.bulk_create(batch, batch_size)

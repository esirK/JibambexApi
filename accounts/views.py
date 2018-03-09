from random import randint

import datetime
import json

from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.authenticaiton import QuietBasicAuthentication
from accounts.models import JibambeUser
from accounts.serializers import LoggedInUser, UserPaymentSerializer, UserSerializer

"""
Receives post requests and updates user account balances 
"""


class AccountTopUp(APIView):
    authentication_classes = (QuietBasicAuthentication,)

    def post(self, request):
        data_to_use = request.body.decode("utf-8")
        data_to_use = data_to_use.replace("'", "\"")
        data_to_use = json.loads(data_to_use)
        print("Received {0}: TYPE: {1}".format(data_to_use, type(data_to_use)))

        user_phone = data_to_use.get('sender_phone')
        user_phone = format_phone_number(user_phone)

        user = user_in_database(user_phone)
        if user:
            updated_user = update_user_details(user, data_to_use)
            return Response(updated_user, status=status.HTTP_200_OK)
        else:
            result, status_code = add_user_to_database(data_to_use)
            return Response(result, status=status_code)


class UserLogin(APIView):
    def post(self, request, format='json'):
        # Check if password and user match
        try:
            user = JibambeUser.objects.get(phone_number=request.data.get('phone_number'))
            if check_password(user, request.data.get('password')):
                if user_is_already_loggedin(user, request):
                    return Response({"message": "Another User Is Already Loggedin With This Credentials"})
                else:
                    # check expire of subscription
                    if (user.subscription_expire - datetime.datetime.now(datetime.timezone.utc)).total_seconds() < 10:
                        # Subscription expired
                        user.subscription_expired = True
                        u = subscribe_user(user)
                        if u is not None:
                            user = u
                            user.loggedin = True
                            user.device_mac = request.data.get('device_mac')
                            user.save()
                            serializer = LoggedInUser(instance=user)
                            return Response(serializer.data)
                        else:
                            user.loggedin = False
                            user.save()
                            return Response({"message": "Subscription Expired and No credit available."
                                                        " Please TopUp your account"})
                    else:
                        user.loggedin = True
                        user.save()
                        serializer = LoggedInUser(user)
                        return Response(serializer.data)

            return Response({"message": "Phone number or password wrong"})
        except Exception as e:
            print(e)
            return Response({"message": "User Does not Exist"})


class Users(APIView):
    """
    Gets all users in the database
    """
    authentication_classes = (QuietBasicAuthentication,)

    def get(self, request):
        if request.user != AnonymousUser:
            users = JibambeUser.objects.all()
            user_s = UserSerializer(users, many=True)
            return Response(user_s.data)
        else:
            return Response({"Not Authenticated"})


"""
Checks if User is already in Database.

Returns the user if found else returns false
"""


def user_in_database(user_phone_number):
    try:
        user = JibambeUser.objects.get(phone_number=user_phone_number)
        if user:
            return user
    except Exception as e:
        return False


def update_user_details(user, data):
    serializer = UserPaymentSerializer(data=data)
    print("Hey LoooooookUpdate {0}".format(serializer.is_valid()))
    # print(serializer.data)
    if serializer.is_valid():
        serializer.save()
        print("Updated Data")
        print(serializer.validated_data)
    else:
        print("Errors")
        print(serializer.errors)
    user.balance = float(user.balance) + float(data.get('amount'))
    user.save()
    response = {"status": "01", "description": "Accepted",
                "subscriber_message": "You ToppedUp Successfully. New Account balance is {0}. Your account details are "
                                      "Phone:{1} Password: {2}".format(user.balance, user.phone_number, user.password)}
    return response


'''
Registers a new user into the Jibambe system
'''


def add_user_to_database(data):
    serializer = UserPaymentSerializer(data=data)
    print("Hey LoooooookAdd {0}".format(serializer.is_valid()))
    # print(serializer.data)
    if serializer.is_valid():
        user = serializer.save()
        print("Saved Data")
        print(serializer.validated_data)
        if user:
            user_data = {}
            user_phone = data.get('sender_phone')
            user_phone = format_phone_number(user_phone)

            user_password = random_4_digit_password(4)
            user_data['phone_number'] = user_phone
            user_data['balance'] = data.get('amount')
            user_data['password'] = user_password

            jibambe_user_serializer = UserSerializer(data=user_data)

            if jibambe_user_serializer.is_valid():
                jibambe_user_serializer.save()
                response = {"status": "01", "description": "Accepted",
                            "subscriber_message": "Welcome to Jibambe na Ma Movie. Your account details are "
                                                  "Phone:{0} Password: {1}".format(user_phone, user_password)}
                return response, status.HTTP_200_OK
            else:
                return jibambe_user_serializer.errors, status.HTTP_400_BAD_REQUEST
    return serializer.errors, status.HTTP_400_BAD_REQUEST


"""
Formats sender phone number from kopokopo response into a number searchable in the database
"""


def format_phone_number(phone_number):
    phone_number = phone_number[4:]
    phone_number = "0" + phone_number
    return phone_number


'''
Determines if a user should be logged in or not
'''


def check_password(user, password):
    if user.password == password:
        return True
    else:
        return False


def subscribe_user(user):
    if user.subscription_expired:
        if float(user.balance) >= 20:
            user.balance = float(user.balance) - 20
            user.subscription_expired = False
            user.subscription_expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
            return user
        else:
            return None


'''
Checks if User is already loggedin and returns true or false on the same. 
'''


def user_is_already_loggedin(user, request):
    if user.loggedin & ((user.subscription_expire -
                         datetime.datetime.now(datetime.timezone.utc)).total_seconds() > 10) \
            & (request.data.get('device_mac') != user.device_mac):
        return True
    else:
        return False


""""
Generates four digit random numbers to be used as password
"""


def random_4_digit_password(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)

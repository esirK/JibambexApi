import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import JibambeUser
from accounts.serializers import UserSerializer, UserLoginSerializer, LoggedInUser

'''
Registers a new user into the Jibambe system
'''


class UserCreate(APIView):
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


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
        if int(user.balance) >= 20:
            user.balance = int(user.balance) - 20
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


class UserLogin(APIView):
    def post(self, request, format='json'):
        # Check if password and user match
        try:
            user = JibambeUser.objects.get(phone_number=request.data.get('phone_number'))
            if check_password(user, request.data.get('password')):
                if user_is_already_loggedin(user, request):
                    return Response({"message": "Another User Is Already Loggedin With This Credentials"},
                                    status=status.HTTP_200_OK)
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
                            return Response({"message": "Subscription Expired and No credit available Please to-up"},
                                            status=status.HTTP_402_PAYMENT_REQUIRED)
                    else:
                        user.loggedin = True
                        user.save()
                        serializer = LoggedInUser(user)
                        return Response(serializer.data)

            return Response({"message": "Phone number or password wrong"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response({"message": "User Does not Exist"}, status=status.HTTP_200_OK)

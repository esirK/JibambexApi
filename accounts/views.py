import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import JibambeUser
from accounts.serializers import UserSerializer, UserLoginSerializer

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


class UserLogin(APIView):
    def post(self, request, format='json'):
        # Check if password and user match
        try:
            user = JibambeUser.objects.get(phone_number=request.data.get('phone_number'))
            if check_password(user, request.data.get('password')):
                if user.loggedin & ((user.subscription_expire -
                                     datetime.datetime.now(datetime.timezone.utc)).total_seconds() > 10):
                    return Response({"message": "Users Already Loggedin"}, status=status.HTTP_200_OK)
                else:
                    # check expire of subscription
                    if (user.subscription_expire - datetime.datetime.now(datetime.timezone.utc)).total_seconds() < 10:
                        # Subscription expired
                        user.subscription_expired = True
                        u = subscribe_user(user)
                        if u is not None:
                            user = u
                            user.loggedin = True
                            user.save()
                            return Response({"message": "Logged in Successfully"}, status=status.HTTP_200_OK)
                        else:
                            user.loggedin = False
                            user.save()
                            return Response({"message": "Subscription Expired and No credit available Please to-up"},
                                            status=status.HTTP_402_PAYMENT_REQUIRED)
                    else:
                        user.loggedin = True
                        user.save()
                        return Response({"message": "Logged in Successfully"}, status=status.HTTP_200_OK)

            return Response({"message": "Phone number or password wrong"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response({"message": "Users Does not Exist"}, status=status.HTTP_200_OK)

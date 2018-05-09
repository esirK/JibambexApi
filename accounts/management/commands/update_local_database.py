import json

import os
import requests
from django.core.management import BaseCommand
from requests.auth import HTTPBasicAuth

from accounts.models import JibambeUser
from accounts.serializers import UserSerializer


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Load Upstream Database to the local Db
        users = requests.get("https://jibambe-kopokopo.herokuapp.com/users",
                             auth=HTTPBasicAuth(username=os.getenv("USERNAME"), password=os.getenv("PASSWORD")))
        print("Received {0}".format(users))
        current_users = JibambeUser.objects.all()
        serialized_users = UserSerializer(current_users, many=True)

        local_users = serialized_users.data

        online_users = users.content.decode('utf-8')
        online_users = json.loads(online_users)

        users_to_update = []

        for user in online_users:
            if self.update_user(user, local_users):
                users_to_update.append(user)
        print("All users updated are {0}".format(users_to_update))

    def update_user(self, online_user, users):
        found = False
        for local_user in users:
            if local_user.get("phone_number") == online_user.get("phone_number"):
                found = True
                print("Updating {0} balance to {1}".format(local_user, online_user))
                user_to_update = JibambeUser.objects.get(phone_number=local_user.get("phone_number"))

                if float(user_to_update.online_balance) == float(online_user.get("balance")):
                    return
                else:
                    user_to_update.balance = float(user_to_update.balance) + (float(online_user.get("balance"))
                                                                              - float(user_to_update.online_balance))
                    user_to_update.previous_balance = user_to_update.balance
                    user_to_update.online_balance = online_user.get("balance")
                    user_to_update.save()

        if found:
            print("User Exists. Just an Update")
            return True
        else:
            online_user['previous_balance'] = online_user.get("balance")
            online_user['online_balance'] = online_user.get("balance")
            add_user_serializer = UserSerializer(data=online_user)
            if add_user_serializer.is_valid():
                add_user_serializer.save()
            else:
                print("User not valid {0}".format(add_user_serializer.errors))
            return False

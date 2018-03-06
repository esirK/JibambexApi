from django.db import models
import datetime


class JibambeUser(models.Model):
    phone_number = models.CharField(unique=True, null=False, max_length=100)
    password = models.CharField(null=False, max_length=100)
    balance = models.CharField(default=0, max_length=100)
    loggedin = models.BooleanField(default=False)
    subscription_expired = models.BooleanField(default=True)
    subscription_expire = models.DateTimeField(default=datetime.datetime(1994, 3, 6, 6, 2, 53, 59037))
    device_mac = models.CharField(unique=False, default='00:00:00:00', max_length=100)

    def __str__(self):
        return self.phone_number

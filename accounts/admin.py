from django.contrib import admin

from .models import JibambeUser, JibambePayment

admin.site.register(JibambeUser)
admin.site.register(JibambePayment)

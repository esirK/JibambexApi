# Generated by Django 2.0.1 on 2018-03-06 01:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20180305_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='jibambeuser',
            name='expire',
            field=models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(hours=24)),
        ),
    ]

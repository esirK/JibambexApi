# Generated by Django 2.0.1 on 2018-03-05 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_jibambeuser_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='jibambeuser',
            name='loggedin',
            field=models.BooleanField(default=False),
        ),
    ]

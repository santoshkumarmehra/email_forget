# Generated by Django 4.1.3 on 2022-12-01 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_validation', '0003_remove_otp_username_otp_email_alter_otp_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

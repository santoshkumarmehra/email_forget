# Generated by Django 4.1.3 on 2022-12-01 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_validation', '0005_alter_otp_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp',
            name='date',
        ),
        migrations.AddField(
            model_name='otp',
            name='time',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]
# Generated by Django 4.1.3 on 2022-12-05 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_validation', '0011_alter_otp_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='otp_time',
            field=models.IntegerField(null=True),
        ),
    ]
# Generated by Django 4.1.3 on 2022-12-01 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_validation', '0009_alter_otp_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='time',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
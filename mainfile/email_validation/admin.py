from django.contrib import admin
from .models import Otp


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ['id','email', 'otp', 'time']


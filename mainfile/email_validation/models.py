from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import datetime, timedelta, date
from django.utils.timezone import now
from django.utils import timezone



class Otp(models.Model):
    email = models.EmailField(max_length=100, null=True)
    otp = models.CharField(max_length=10, null=True)
    time = models.DateTimeField(auto_now_add=True, null=True)

    


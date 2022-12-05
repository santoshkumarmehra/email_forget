from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .helpers import send_forget_password_mail
from django.contrib import messages
import random
from .models import Otp
import time
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


def signup(request):
    if request.method == "POST":    
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        User(username=username, email=email, password=password).save()
    return render(request, 'signup.html')


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        data = User.objects.all()
        for data in data:
            if data.email == email and data.password == password:
                return redirect('profile')
        return render(request, 'login.html')
    return render(request, 'login.html')


def profile(request):   
    return render(request, 'profile.html')


def otp(request, id):    
    # otp_user = User.objects.get(id=id)
    # user_email = otp_user.email
    # otp_time = Otp.objects.get(email=user_email)
    # old_otp_time = otp_time.otp_time
    # new_otp_time = time.time()
    # total_time = new_otp_time - old_otp_time    
    if request.method == "POST":
        otp = request.POST.get('otp')
        if not otp.isdigit():
            messages.info(request, 'fill correclty')
            return render(request, 'otp.html', {'id':id})
        elif len(otp)<4 or len(otp)>4:
            messages.info(request, 'fill correclty')
            return render(request, 'otp.html', {'id':id})
        user = Otp.objects.filter(otp=otp)        
        if not user:
            messages.info(request, 'fill correclty')
            return render(request, 'otp.html', {'id':id})
        else:
            for userdata in user:
                    if userdata.otp == otp:               
                        return redirect('password_change', id) 
            return render(request, 'otp.html', {'id':id})
    return render(request, 'otp.html', {'id':id})           


def password_change(request, id):   
    if request.method =="POST":
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')    
        if password != confirmpassword:
            messages.info(request, 'Password didn"t match !!!')
            return render(request, 'password_change.html', {'otp':otp})           
        else:
            id = int(id)
            found_email = User.objects.filter(id=id).get()
            for_serach_found_email = found_email.email
            userdata = Otp.objects.get(email=for_serach_found_email)
            email = userdata.email             
            original_email = User.objects.filter(email=email).get()
            original_email.password = password
            original_email.save()
            messages.success(request, 'Password has been changed !!!')
            return redirect('/login/')            
    return render(request, 'password_change.html', {'id':id})


def delete_after_one_minutes():
    global email
    time.sleep(24)
    user_temporary = Otp.objects.get(email=email)
    user_temporary.otp = None
    user_temporary.save()
    return True
            

def password_reset(request):
    global otpgenerationtime
    if request.method == "POST":
        #otpinsertiontime
        global email
        email = request.POST.get('email')        
        if not User.objects.filter(email=email):       
            messages.warning(request, 'Your account is not exists !!!')     
            return redirect('/password_reset/')
        else:               
            otp = ''
            number = random.sample(set(range(10, 99)), 2)
            for otpnumber in number:
                otp += str(otpnumber)
            user1 = User.objects.get(email=email)
            user_temporary = Otp.objects.filter(email=user1.email)
            otp_time = time.time()
            if not user_temporary:               
                Otp(email=user1.email, otp=otp, time=datetime.now().strftime('%Y:%b:%d %H:%M:%S'), otp_time=otp_time).save() 
                user_temporary = Otp.objects.filter(email=user1.email).get()
                send_forget_password_mail(user_temporary.email, user_temporary.otp, user1.id)
                scheduler = BackgroundScheduler()
                scheduler.add_job(delete_after_one_minutes, 'interval', seconds=24)
                scheduler.start()
                return render(request, 'password_reset.html')
            else:
                user_temporary = Otp.objects.get(email=email)
                user_temporary.otp = otp
                user_temporary.otp_time = otp_time  
                user_temporary.save()                
                send_forget_password_mail(user_temporary.email, user_temporary.otp, user1.id)
                scheduler = BackgroundScheduler()
                scheduler.add_job(delete_after_one_minutes, 'interval', seconds=20)
                scheduler.start()              
                return render(request, 'password_reset.html')                
    return render(request, 'password_reset.html')




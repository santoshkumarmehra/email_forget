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
            # time_verification = Otp.objects.get(id=id)
            # print(time_verification)
            # user = User.objects.filter(id=id).get()
            # email = user.email
            # time_verification = Otp.objects.get(email=email)
            # str_value_time = time_verification.time
            # list_existing_time = str(str_value_time).split(" ")
            # list_existing_time1 = list_existing_time[1].split(":")
            # for time in list_existing_time1[2:3]:
            #     value = time.split(".")[0:1]
            #     value1 = value[0]
            #     list_existing_time1.insert(2,value1)
            # # print(list_existing_time)
            # evaulate_list = [value for value in list_existing_time1[:3]]
            # print(evaulate_list)           
            # str_value_time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S').split(" ")
            # str_value_time_now1 = str_value_time_now[1].split(":")
            # print(str_value_time_now1)
            # if list_existing_time[0] != str_value_time_now[0]:
            #     print("phase-1")
            #     return render(request, 'otp.html', {'id':id})
            # if evaulate_list[0] != str_value_time_now1[0]:
            #     print("phase-2")
            #     return render(request, 'otp.html', {'id':id})
            # elif (evaulate_list[1] != str_value_time_now1[1]) or (evaulate_list[1] == str_value_time_now1[1]):
            #     print("hello")
                # user = User.objects.filter(id=id).get()
                # email = user.email
                # time = Otp.objects.get(email=email)
                # time.time = datetime.now()
                # time.save()
    
                # Otp(time=datetime.now().strftime('%Y:%m:%d %H:%M:%S')).save()
                # alltime = Otp.objects.all().update(time=datetime.now())

                # alltime.datetime.now().strftime('%Y:%m:%d %H:%M:%S')
                # alltime.save()
                # print('hello')

                                                    
            #     print("phase-3")
            #     return render(request, 'otp.html', {'id':id})



            # elif evaulate_list[2] != str_value_time_now1[2]:
            #     print("phase-4")
            #     return render(request, 'otp.html', {'id':id})

            
            # else:
                # for userdata in user:
                #     if userdata.otp == otp:               
                #         return redirect('password_change', id)                         
    # return render(request, 'otp.html', {'id':id})


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
    time.sleep(20)
    user_temporary = Otp.objects.get(email=email)
    user_temporary.otp = None
    user_temporary.save()
    return True
            

def password_reset(request):
    if request.method == "POST":
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
            Otp(email=user1.email, otp=otp, time=datetime.now().strftime('%Y:%b:%d %H:%M:%S')).save() 
            user_temporary = Otp.objects.get(email=email)  
            if user1.email == user_temporary.email:
                otpsave = Otp.objects.get(email=email)  #for existing user
                otpsave.otp = otp
                otpsave.save()                
                send_forget_password_mail(email, otp, user1.id)
                scheduler = BackgroundScheduler()
                scheduler.add_job(delete_after_one_minutes, 'interval', seconds=20)
                scheduler.start()
                return render(request, 'password_reset.html')                

            else:
                Otp(email=user1.email, otp=otp).save()    #for new user        
                send_forget_password_mail(email, otp, user1.id)
                return render(request, 'password_reset.html')
    return render(request, 'password_reset.html')




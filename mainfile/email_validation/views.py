from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .helpers import send_forget_password_mail
from django.contrib import messages


def signup(request):
    if request.method == "POST":
        # data = request.POST
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
    # print(request.user)  
    return render(request, 'profile.html')


def password_reset(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if not User.objects.filter(email=email):       
            messages.warning(request, 'Your account is not exists !!!')     
            return redirect('/password_reset/')
        else:    
            email_id = User.objects.filter(email=email)
            id=0
            for id in email_id:                
                id = id.id
            send_forget_password_mail(email, id)
    return render(request, 'password_reset.html')


def password_change(request, id):   
    if request.method =="POST":
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')    
        if password != confirmpassword:
            messages.info(request, 'Password didn"t match !!!')
            return render(request, 'password_change.html', {'id':id})
        else:
            id = int(id)
            userdata = User.objects.get(id=id)
            userdata.password = password
            userdata.save()                        
            messages.success(request, 'Password has been changed !!!')
            return redirect('/login/')            
    return render(request, 'password_change.html', {'id':id})
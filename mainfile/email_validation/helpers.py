from django.core.mail import send_mail

from django.conf import settings

def send_forget_password_mail(email, id):
    subject = 'Your password link'
    message = f'''hi, click on the link to reset your password 
    http://127.0.0.1:8000/password_change/{id}/'''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


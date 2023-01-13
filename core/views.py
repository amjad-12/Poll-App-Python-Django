# pylint: disable=no-else-return
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import User
from polls.models import Customer
from django.contrib import messages
from myPolls import settings
from django.core.mail import send_mail


# Create your views here.
def home(request):
    return render(request, 'core/index.html')

def signup(request):
    if request.method == "POST":
        # username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        phone = request.POST['phone']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
            
        if pass1 != pass2:
            messages.error(request, "Password didn't match!")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        
        customer = Customer.objects.create(user_id=myuser.id, phone=phone)

        myuser.save()

        messages.success(request, "Your Account has been successfully created")


        # Welcome Email

        subject = "Welcome to my djnago app"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to my django app!! \n Thank you for visiting us \n We have also sent you a confirmation email, please confirm your email address to activate you account"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)


        return redirect('signin')

    return render(request, "core/signup.html")

def signin(request):
    if request.method == 'POST':
        # email = request.POST['email']
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'core/index.html', {'fname': fname})
        
        else:
            messages.error(request, 'Bad Cradentials!')
            return redirect('home')

    return render(request, "core/signin.html")

def signout(request):
    logout(request)
    messages.success(request, 'Logged Out Succccesfully')
    return redirect('home')

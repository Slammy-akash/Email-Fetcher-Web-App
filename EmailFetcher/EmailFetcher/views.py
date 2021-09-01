#created by Akash
import imaplib
import email
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login



def index(request):
    return render(request, 'index.html')

def handlelogin(request):
    if request.method == "POST":
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request, user)
            #return render(request, 'ReadMail/index.html')
            return redirect('ReadMail/')
        else:
            return render(request,'index.html', {'error':'Invalid Username or Password'})
    return HttpResponse('404 Page Not Found')




from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.shortcuts import render, redirect
from .forms import SignUP
from django.contrib.auth import authenticate, login

@login_required
def sign_up(request):
    if request.user.profile.type == "School":
        if request.method == 'POST':
            Form = SignUP(request.POST)
            if Form.is_valid():
                instance = Form.save()
                # type = request.POST["type"]
                type = "Teacher"
                instance.profile.type = type
                if type == "Teacher":
                    instance.profile.school = request.user.profile
                    instance.save()
                instance.profile.save()
                username = Form.cleaned_data['username']
                password = Form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect(f'/')
        else:
            Form = SignUP()
        return render(request, 'registration/sign_up.html', {'form': Form})
    else:
        return redirect("/error")

from django.shortcuts import render, redirect
from .register_form import RegisterForm
from django.contrib import messages


def registration_ok(request):
    return render(request, 'registration/registration_ok.html')


def logged_out(request):
    return render(request, 'registration/logged_out.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # appears only in /admin :
            messages.success(request, 'Account created successfully')
            return redirect('registration_ok')
    else:
        form = RegisterForm()
    context = {
        "form": form
    }
    return render(request, 'registration/register.html', context)

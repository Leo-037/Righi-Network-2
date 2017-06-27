from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
)
from django.shortcuts import render, redirect

from .forms import UserLoginForm  # , SignUpForm, ClasseForm

User = get_user_model()


# Create your views here.

def login_view(request):
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if user.studente.is_attivato:
            if next:
                return redirect(next)
            return redirect("/")
        else:
            return redirect("/gestione/aggiorna/email/")

    return render(request, "account/login.html", {"form": form, "title": title})

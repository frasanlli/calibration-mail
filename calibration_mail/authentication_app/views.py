from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.

def log_in(request):
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username = username,
                                password = password)
            if user is not None:
                login(request, user)
                redirect("tools/tools_state.html")
            else:
                for msg in form.error_messages:
                    messages.error(request, form.error_messages[msg])

        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages)

    return render(request, "authentication_app/log_in.html", {"form": form})

@login_required
def log_out(request):
    logout(request)

    return redirect("authentication_app/log_in.html")
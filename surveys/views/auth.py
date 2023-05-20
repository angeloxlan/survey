from django.contrib.auth import logout as logout_handler
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse


def signup(request):
    if request.user.is_authenticated:
        return redirect('list-surveys')

    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()

            return redirect('list-surveys')
    else:
        user_form = UserCreationForm()

    context = {
        'user_form': user_form
    }

    return render(request, 'surveys/auth/signup.html', context)


class AuthLoginView(LoginView):
    template_name = 'surveys/auth/login.html'
    redirect_authenticated_user = True

login = AuthLoginView.as_view()


def logout(request):
    logout_handler(request)
    return redirect('login')

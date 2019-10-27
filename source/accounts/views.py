from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from accounts.forms import UserCreationForm


def login_view(request):
    context = {}
    next = request.GET.get('next')
    redirect_url = request.session.setdefault('url', next)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if redirect_url:
                return redirect(redirect_url)
            else:
                return redirect('webapp:index')
        else:
            context['has_error'] = True
    return render(request, 'login.html', context=context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('webapp:index')

def register_view(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'register.html', {'form':form})
    elif request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data['username'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('webapp:index')
        else:
            return render(request, 'register.html', {'form':form})


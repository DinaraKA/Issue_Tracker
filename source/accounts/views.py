from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView, UpdateView, ListView
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.forms import UserCreationForm, UserInfoChangeForm, UserPasswordChangeForm
from accounts.models import Token
from main.settings import HOST_NAME


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
            user = User(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                is_active=False
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            token = Token.objects.create(user=user)
            activation_url= HOST_NAME + reverse('accounts:user_activate') + '?token={}'.format(token)
            user.email_user('Registration on site localhost', 'For activation go to link: {}'.format(activation_url))
            return redirect('webapp:index')
        else:
            return render(request, 'register.html', {'form':form})


def user_activate(request):
    token_value = request.GET.get('token')
    try:
        token = Token.objects.get(token=token_value)
        user = token.user
        user.is_active = True
        user.save()
        token.delete()
        login(request, user)
        return redirect('webapp:index')
    except Token.DoesNotExist:
        return redirect('webapp:index')


class UserIndexView(ListView):
    context_object_name = 'user_objects'
    model = User
    template_name = 'user_index.html'
    paginate_by = 5
    paginate_orphans = 1


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_object'


class UserInfoChangeView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_update.html'
    context_object_name = 'user_object'
    form_class = UserInfoChangeForm

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.object.pk})


class UserPasswordChangeView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_password_change.html'
    form_class = UserPasswordChangeForm
    context_object_name = 'user_object'

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:login')



from django.shortcuts import render, HttpResponseRedirect
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from django.contrib import auth
from django.urls import reverse
from django.contrib import messages
from basketapp.models import Basket
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import User

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'title': 'GeekShop - Авторизация', 'form': form}
    return render(request, 'authapp/login.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'Данные успешно обновлены!')
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)
    baskets = Basket.objects.filter(user=request.user)
    context = {'title': 'GeekShop - Личный кабинет',
               'baskets' : baskets,
               'total_quantity' : baskets.first().total_quantity() if baskets else 0,
               'total_sum': baskets.first().total_sum() if baskets else 0,
               'form': form,
               'profile_form': profile_form}
    return render(request, 'authapp/profile.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            send_verify_link(user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
    context = {'title': 'GeekShop - Регистрация', 'form': form}
    return render(request, 'authapp/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def send_verify_link(user):
    verify_link = reverse('users:verify',args=[user.email, user.activation_key])
    subject = 'Account verify'
    message = f'Your link for account activation: {settings.DOMAIN_NAME}{verify_link}'
    return  send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

def verify(request, email, key):
    user = User.objects.filter(email=email).first()
    if user and user.activation_key == key and not user.is_activation_key_expired():
        user.is_active = True
        user.activation_key = ''
        user.activation_key_created = None
        user.save()
        auth.login(request, user)
    return render(request, 'authapp/verify.html')
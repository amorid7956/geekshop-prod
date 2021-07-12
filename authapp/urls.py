from django.urls import path
from .views import login, register, logout, profile, verify

app_name = 'authapp'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<email>/<key>/', verify, name='verify'),
]
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/password/', views.password, name='password'),
    path('profile/<nickname>/', views.profile, name='profile'),
    path('profile/<nickname>/like/', views.mylike, name='mylike'),
    path('profile/<nickname>/later/', views.mylater, name='mylater'),
    path('profile/<nickname>/stats/', views.mystats, name='mystats'),
    path('alarm/', views.password_alarm, name='password_alarm'),
]

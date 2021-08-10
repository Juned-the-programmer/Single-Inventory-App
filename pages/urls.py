from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('signup_gst',views.signup_gst,name="signup_gst"),
    path('signup_estimate',views.signup_estimate,name="signup_estimate"),
    path('profile',views.profile,name="profile"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('logout',views.logout,name="logout"),
    path('error404',views.error404,name="error404"),
    path('user_name',views.user_name,name="user_name")
]

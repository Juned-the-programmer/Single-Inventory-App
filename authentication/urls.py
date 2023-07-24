from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login,name='login'),
    path('signup-gst',views.signup_gst,name="signup_gst"),
    path('signup-estimate',views.signup_estimate,name="signup_estimate"),
    path('logout',views.logout,name="logout"),
]

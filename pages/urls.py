from django.urls import path
from . import views

urlpatterns = [
    path('profile',views.profile,name="profile"),
    path('error404',views.error404,name="error404"),
    path('user_name',views.user_name,name="user_name")
]

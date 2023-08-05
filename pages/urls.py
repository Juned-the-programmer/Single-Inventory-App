from django.urls import path
from . import views

urlpatterns = [
    path('profile',views.profile,name="profile"),
    path('error404',views.error404,name="error404"),
    path('user_name',views.user_name,name="user_name"),
    path('export_backup/', views.export_backup, name='export_backup'),
    path('backup/', views.backup_page, name='backup_page'),
]

from django.urls import path
from . import views

urlpatterns = [
     path('addsupplier/',views.addsupplier,name="addsupplier"),
    path('viewsupplier/',views.viewsupplier,name="viewsupplier"),
    path('updatesupplier/<pk>',views.updatesupplier,name="updatesupplier"),
]

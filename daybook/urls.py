from django.urls import path
from . import views

urlpatterns = [
     path('dailyincome/',views.dailyincome,name="dailyincome"),
    path('dailyexpense/',views.dailyexpense,name="dailyexpense"),
]

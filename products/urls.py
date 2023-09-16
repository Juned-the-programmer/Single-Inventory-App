from django.urls import path
from . import views

urlpatterns = [
    path('addproduct/',views.addproduct,name="addproduct"),
    path('viewproduct/',views.viewproduct,name="viewproduct"),
    path('updateproduct/<pk>',views.updateproduct,name="updateproduct"),
    path('manufacture/required', views.product_required, name="manufactureproductrequired"),
    path('manufacture/product',views.manufacture_product, name="manufacureproduct")
]

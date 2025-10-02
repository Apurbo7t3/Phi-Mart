from django.urls import path,include
from product import views
urlpatterns = [
    path('',views.ProductList.as_view(),name='product-list'),
     path('<int:pk>/',views.ProductDetails.as_view(),name='view-sepecific-product'),
]

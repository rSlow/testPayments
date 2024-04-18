from django.urls import path

from .views import AddProductInCartAPIView, CartAPIView

urlpatterns = [
    path('add/', AddProductInCartAPIView.as_view(), name='add_product_in_cart'),
    path('<int:user_id>/', CartAPIView.as_view(), name='cart'),
]

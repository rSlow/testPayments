from django.urls import path

from .views import AddProductCartAPIView

urlpatterns = [
    path('cart/<int:user>/<int:product>/', AddProductCartAPIView.as_view(), name='add_product_in_cart'),
]

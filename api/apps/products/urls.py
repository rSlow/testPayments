from django.urls import path

from .views import CategoriesAPIView, SubCategoriesAPIView, ProductsAPIView, ProductAPIView

urlpatterns = [
    path('categories/', CategoriesAPIView.as_view(), name='categories'),
    path('categories/<int:category>/', SubCategoriesAPIView.as_view(), name='subcategories'),
    path('categories/<int:category>/<int:subcategory>/', ProductsAPIView.as_view(), name='products'),
    path('product/<int:product>/', ProductAPIView.as_view(), name='product'),
]

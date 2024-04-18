from django.urls import path

from .views import CategoriesAPIView, CategoryAPIView, SubCategoryAPIView, ProductAPIView

urlpatterns = [
    path('category/', CategoriesAPIView.as_view(), name='categories'),
    path('category/<int:category>/', CategoryAPIView.as_view(), name='category'),
    path('subcategory/<int:subcategory>/', SubCategoryAPIView.as_view(), name='subcategory'),
    path('<int:product>/', ProductAPIView.as_view(), name='product'),
]

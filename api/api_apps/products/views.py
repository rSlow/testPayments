from rest_framework.generics import ListAPIView, RetrieveAPIView

from api_apps.products.models import Category, SubCategory
from api_apps.products.serializers import (CategorySerializer,
                                           CategoryRelatedSerializer,
                                           SubCategoryRelatedSerializer,
                                           ProductSerializer)


class CategoriesAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryAPIView(RetrieveAPIView):
    serializer_class = CategoryRelatedSerializer
    queryset = Category.objects.prefetch_related("subcategories")
    lookup_url_kwarg = "category"


class SubCategoryAPIView(RetrieveAPIView):
    serializer_class = SubCategoryRelatedSerializer
    queryset = SubCategory.objects.prefetch_related("products")
    lookup_url_kwarg = "subcategory"


class ProductAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = ProductSerializer.Meta.model.objects.all()
    lookup_url_kwarg = "product"

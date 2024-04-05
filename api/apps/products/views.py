from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.products.serializers import CategorySerializer, SubCategorySerializer, ProductSerializer


class CategoriesAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = CategorySerializer.Meta.model.objects.all()


class SubCategoriesAPIView(ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        category_pk = self.kwargs["category"]
        return self.serializer_class.Meta.model.objects.filter(category_id=category_pk)


class ProductsAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_pk = self.kwargs["category"]
        subcategory_pk = self.kwargs["subcategory"]
        return self.serializer_class.Meta.model.objects.filter(
            subcategory_id=subcategory_pk,
            subcategory__category_id=category_pk
        )


class ProductAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = ProductSerializer.Meta.model.objects.all()
    lookup_url_kwarg = "product"

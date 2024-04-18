from rest_framework.serializers import ModelSerializer

from ..models import SubCategory
from .product import ProductSerializer


class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["pk", "name"]


class SubCategoryRelatedSerializer(SubCategorySerializer):
    products = ProductSerializer(many=True)

    class Meta(SubCategorySerializer.Meta):
        fields = ["pk", "name", "products"]

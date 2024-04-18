from rest_framework.serializers import ModelSerializer

from .subcategory import SubCategorySerializer
from ..models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["pk", "name"]


class CategoryRelatedSerializer(CategorySerializer):
    subcategories = SubCategorySerializer(many=True)

    class Meta(CategorySerializer.Meta):
        fields = ["pk", "name", "subcategories"]

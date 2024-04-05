from rest_framework.serializers import ModelSerializer

from .models import Category, SubCategory, Product


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["pk", "name"]


class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["pk", "name"]


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["pk", "title", "description", "photo"]

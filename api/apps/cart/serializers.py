from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from .models import UserCart
from ..products.models import Product


class CartSerializer(ModelSerializer):
    products = PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        many=True
    )

    class Meta:
        model = UserCart
        fields = ["pk", "user", "products"]


class ProductSerializer(ModelSerializer):
    cart_list = CartSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["pk", "cart_list"]

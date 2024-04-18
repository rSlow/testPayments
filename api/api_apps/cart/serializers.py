from rest_framework.serializers import ModelSerializer

from .models import ProductInCart, UserCart


class ProductInCartSerializer(ModelSerializer):
    class Meta:
        model = ProductInCart
        fields = ["product", "count"]


class CartSerializer(ModelSerializer):
    products = ProductInCartSerializer(many=True)

    class Meta:
        depth = 1
        model = UserCart
        fields = ["user_id", "pk", "products"]

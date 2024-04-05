from rest_framework.generics import CreateAPIView

from .serializers import CartSerializer


class AddProductCartAPIView(CreateAPIView):
    serializer_class = CartSerializer

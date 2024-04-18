from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import UserCart, ProductInCart
from .serializers import ProductInCartSerializer, CartSerializer


class CartAPIView(CreateAPIView,
                  RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    queryset = UserCart.objects.all()
    lookup_field = "user_id"
    lookup_url_kwarg = "user_id"


class AddProductInCartAPIView(CreateAPIView):
    serializer_class = ProductInCartSerializer
    queryset = ProductInCart.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

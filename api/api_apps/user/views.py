from rest_framework.generics import RetrieveAPIView, CreateAPIView

from api_apps.user.serializers import UserSerializer

from api_apps.user.models import TelegramUser


# Create your views here.


class UserAPIView(CreateAPIView,
                  RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = TelegramUser.objects.all()
    lookup_url_kwarg = "user_id"

    def get_object(self):
        telegram_id = self.kwargs[self.lookup_url_kwarg]
        obj = self.queryset.filter(telegram_id=telegram_id).first()
        if not obj:
            serializer: UserSerializer = self.get_serializer(data={"telegram_id": telegram_id})
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
        return obj

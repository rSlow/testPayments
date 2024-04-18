from rest_framework.serializers import ModelSerializer

from api_apps.user.models import TelegramUser


class UserSerializer(ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ["pk", "telegram_id", "is_active"]

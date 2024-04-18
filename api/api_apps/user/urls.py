from django.urls import path

from .views import UserAPIView

urlpatterns = [
    path('<int:user_id>/', UserAPIView.as_view(), name='users'),
]

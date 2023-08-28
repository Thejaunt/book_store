from django.urls import path, include

from .views import RegisterApi

from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("auth/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", RegisterApi.as_view()),
]

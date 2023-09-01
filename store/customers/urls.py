from django.urls import path, include

from .views import RegisterApi, CustomerLoginAPIView, CustomerLogoutAPIView

from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterApi.as_view(), name="register"),
    path("login/", CustomerLoginAPIView.as_view(), name="login"),
    path("logout/", CustomerLogoutAPIView.as_view(), name="logout"),
]

from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CustomerSerializer, RegisterSerializer, CustomerLoginSerializer


class RegisterApi(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        token = RefreshToken.for_user(customer)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)


class CustomerLoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomerLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.validated_data
        serializer = CustomerSerializer(customer)
        token = RefreshToken.for_user(customer)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        resp = Response()
        resp.data = data
        resp.set_cookie(key="jwt", value=str(token))
        resp.status = status.HTTP_200_OK

        return resp


class CustomerLogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)

        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

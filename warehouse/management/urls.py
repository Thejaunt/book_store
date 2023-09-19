from django.urls import path
from .views import db_update, new_order_view


urlpatterns = [
    path("new_order/", new_order_view, name="new-order"),
    path("db_update/", db_update),
]

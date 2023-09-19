from celery import shared_task
from celery import Celery
import requests

from .serializers import WarehouseSerializer
from .models import Book


@shared_task()
def send_new_order(data):
    res = requests.post("http://localhost:8002/new_order/", json=data)


@shared_task()
def db_update():
    store_data = Book.objects.all()
    resp = requests.get("http://localhost:8002/db_update/")
    ser = WarehouseSerializer(data=resp.json()["data"], many=True)
    ser.is_valid(raise_exception=True)

    # making dict where keys are warehouse ids
    data_dict = {}
    for b in ser.validated_data:
        book = dict(b)
        data_dict[int(book.get('id'))] = {
            "title": f"{book.get('title')}",
            "price": round(float(book.get('price')), 2),
            "quantity": int(book.get('quantity')),
        }

    # updating & deleting existing books by warehouse id
    warehouse_ids = list(data_dict.keys())
    warehouse_ids_in_store = []
    for store_book in store_data:
        # has to be optimized - bulk_update
        if store_book.id_warehouse not in warehouse_ids:
            store_book.delete()
            continue
        else:
            warehouse_ids_in_store.append(store_book.id_warehouse)

        store_book.quantity = data_dict[store_book.id_warehouse].get("quantity")
        store_book.price = data_dict[store_book.id_warehouse].get("price")
        store_book.title = data_dict[store_book.id_warehouse].get("title")
        store_book.save()

    for warehouse_id in warehouse_ids:
        # has to be optimized to bulk_create
        if warehouse_id not in warehouse_ids_in_store:
            Book.objects.create(
                title=data_dict[warehouse_id].get("title"),
                price=data_dict[warehouse_id].get("price"),
                quantity=data_dict[warehouse_id].get("price"),
                id_warehouse=warehouse_id
            )

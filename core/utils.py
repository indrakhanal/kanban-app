from rest_framework.decorators import action as drf_action
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import *

def sort_model(model, order_ids=[]):

    if len(order_ids) != len(set(order_ids)):
        return HTTP_400_BAD_REQUEST

    objects = dict(
        [(str(obj.id), obj) for obj in model.objects.filter(id__in=order_ids)]
    )
    order_field_name = model._meta.ordering[0]
    
    step = 1
    start_object = min(objects.values(), key=lambda x: getattr(x, order_field_name))
    start_index = getattr(start_object, order_field_name, len(order_ids))
    print(start_index, start_object)
    for id in order_ids:
        object = objects.get(str(id))
        if getattr(object, order_field_name) != start_index:
            setattr(object, order_field_name, start_index)
            object.save(update_fields=[order_field_name])

        start_index += step

    return HTTP_200_OK

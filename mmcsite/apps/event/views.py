# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import HttpResponseBadRequest
from event.models import IotOrderEvent, IotDeviceEvent
from utils.views import HttpResponseMessage, HttpResponseMessageWithData, dateFormat

from order.models import IotOrder
from device.views import IotDevice


def order_event_to_dict(t):
    t_dict = {
        "id": t.pk,
        "order_id":t.order.pk,
        "type": t.type,
        "extra": t.extra,
        "time": t.time.strftime(dateFormat),
        "description": t.description
    }
    return t_dict

#mmc APIs for device
@csrf_exempt
def order_update_event_post(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
    else:
        return HttpResponseBadRequest('Bad Request')

    if 'order_id' in json_data:
        _order_id = json_data['order_id']
        print _order_id
    else:
        return HttpResponseMessage(1, 'no order id in request')

    _order=None
    try:
        _order=IotOrder.objects.get(pk=_order_id)
    except:
        return HttpResponseMessage(2, 'the order does not exist')

    _type = 2
    _extra = ''
    if 'start_time' in json_data:
        _extra = json_data['start_time']

    if 'end_time' in json_data:
        _extra = json_data['end_time']
        _type = 3

    event = IotOrderEvent.objects.create(
        order=_order,
        type=_type,
        extra=_extra,
    )

    return HttpResponseMessageWithData(0, 'success', "order_event", order_event_to_dict(event))

@csrf_exempt
def get_order_events(request):
    _order_id = request.GET.get('order_id')

    if _order_id is None:
        return HttpResponseMessage(1, 'no order in in request')
    else:
        try:
            print _order_id
            _order = IotOrder.objects.get(pk=_order_id)
            events = _order.order_events.all()
            if len(events)>0:
                event_dist = []
                for t in events:
                    event_dist.append(order_event_to_dict(t))
                return HttpResponseMessageWithData(0, 'success', "events", event_dist)
            else:
                return HttpResponseMessage(1, 'no event assocated with the order')
        except:
            return HttpResponseMessage(1, 'the order id does not exist in db')


@csrf_exempt
def get_all_coming_ips(request):
    print "get_all_coming_ips"
    events = IotOrderEvent.objects.filter(Q(type=2) | Q(type=3))
    print len(events)
    if len(events) > 0:
        event_dist = []
        for t in events:
            if (t.description!='' and t.description!=None):
                #print t.description
                event_dist.append(order_event_to_dict(t))
        return HttpResponseMessageWithData(0, 'success', "events", event_dist)
    else:
        return HttpResponseMessage(1, 'no event assocated with ip')


def device_event_to_dict(t):
    t_dict = {
        "id": t.pk,
        "mac":t.device.mac_addr,
        "type": t.type,
        "extra": t.extra,
        "time": t.time.strftime(dateFormat),
    }
    return t_dict

@csrf_exempt
def device_update_event_post(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
    else:
        return HttpResponseBadRequest('Bad Request')

    if 'mac' in json_data:
        _mac = json_data['mac']
    else:
        return HttpResponseMessage(1, 'no mac id in request')

    _device=None
    try:
        _device=IotDevice.objects.get(mac_addr=_mac)
    except:
        return HttpResponseMessage(2, 'the order does not exist')

    _extra = ''
    if 'battery_level' in json_data:
        _battery = json_data['battery_level']

    event = IotDeviceEvent.objects.create(
        device=_device,
        extra=str(_battery),
    )

    return HttpResponseMessageWithData(0, 'success', "device_event", device_event_to_dict(event))




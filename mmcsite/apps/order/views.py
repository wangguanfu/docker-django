import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from datetime import datetime
from temperature.models import IotTemp
from express.models import IotExpress
from device.models import IotDevice

from utils.views import HttpResponseMessage, HttpResponseMessageWithData, dateFormat, logger
from order.models import IotOrder, STATUS_INIT, STATUS_DONE, STATUS_ALL, NOT_VALID_TEMPERATURE
from event.models import IotOrderEvent


def t_to_dict(t):
    if t.device is None:
        _mac = t.mac
    else:
        _mac = t.device.mac_addr
    if t.express is None:
        _number = t.number
    else:
        _number = t.express.number
    if t.end_time is not None:
        _endtime = t.end_time.strftime(dateFormat)
    else:
        _endtime = ''
    t_dict = {
        "order_id": t.pk,
        "mac": _mac,
        "number": _number,
        "start_time": t.start_time.strftime(dateFormat),
        "end_time": _endtime,
        "create_time": t.create_time.strftime(dateFormat),
        "high_temp": t.high_temp,
        "low_temp": t.low_temp,
        "highest_temp": t.highest_temp,
        "lowest_temp": t.lowest_temp,
        "status": t.status,
        "coordinate": t.coordinate,
    }
    return t_dict


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# mmc APIs for express
@csrf_exempt
def register(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
    else:
        return HttpResponseBadRequest('Bad Request')

    # print "%s" %(json_data)

    if 'mac' in json_data:
        _mac = json_data['mac']
        try:
            _device = IotDevice.objects.get(mac_addr=_mac)
            # filter
            # _device = IotDevice.objects.filter(mac_addr=_mac).first()
        except:
            _device = None
            # print "the device is exists----> "
            # return HttpResponseMessage(8, 'mac is exists')
    else:
        return HttpResponseMessage(1, 'no mac in request')

    if 'number' in json_data:
        _number = json_data['number']
        try:
            _express = IotExpress.objects.get(number=_number)
            # _express = IotExpress.objects.filter(number=_number).first()
        except:
            _express = None
            # print "the number is exists----> "
            # return HttpResponseMessage(9, 'express is exists')
    else:
        return HttpResponseMessage(2, 'no express info in request')

    # start_time is set in register, can not be updated later
    if 'start_time' in json_data:
        _starttime = json_data['start_time']
        # return HttpResponseMessage(3, _starttime)
        try:
            start = datetime.strptime(_starttime, dateFormat)
        except:
            return HttpResponseMessage(4, 'start time not correct')
    else:
        return HttpResponseMessage(3, 'no start time in request')
    # express = IotExpress.objects.get(number=_number)

    if 'end_time' in json_data:
        _endtime = json_data['end_time']
        try:
            end = datetime.strptime(_endtime, dateFormat)
        except:
            return HttpResponseMessage(5, 'end time not correct')
    else:
        end = None

    if 'high_temp' in json_data:
        _hightemp = json_data['high_temp']
    else:
        return HttpResponseMessage(6, 'no high temperature set')

    if 'low_temp' in json_data:
        _lowtemp = json_data['low_temp']
    else:
        return HttpResponseMessage(7, "no low temperature set")

    if 'coordinate' in json_data:
        _coordinate = json_data['coordinate']
    else:
        _coordinate = STATUS_INIT

    if 'status' in json_data:
        _status = json_data['status']
    else:
        _status = STATUS_INIT

    _type = 2
    if _status == STATUS_DONE:
        data = gethighlow(_mac, start, end)
        _highest = data['highest']
        _lowest = data['lowest']
        # EVENT_TYPE_CHOICES
        _type = 3
    else:
        _highest = NOT_VALID_TEMPERATURE
        _lowest = NOT_VALID_TEMPERATURE
        _type = 2

    # get_or_create

    _get_order = IotOrder.objects.filter(
        mac=_mac,
        number=_number,
    )

    # check order in db
    if _get_order.count() is not 0:
        print "already created order info about %s , we will update order" % (_mac)
        _updatedb = IotOrder.objects.filter(
            mac=_mac,
            number=_number,
        ).update(
            end_time=end,
            high_temp=_hightemp,
            low_temp=_lowtemp,
            highest_temp=_highest,
            lowest_temp=_lowest,
            status=_status,
            coordinate=_coordinate,
        )
        if _updatedb:
            _order = IotOrder.objects.filter(
                mac=_mac,
                number=_number,
            ).first()
        else:
            return HttpResponseMessage(8, "fatal error occurs in update db")
    else:
        print "does not find order info about %s , we will create order" % (_mac)
        _order = IotOrder.objects.create(
            mac=_mac,
            number=_number,
            device=_device,
            express=_express,
            start_time=start,
            end_time=end,
            high_temp=_hightemp,
            low_temp=_lowtemp,
            highest_temp=_highest,
            lowest_temp=_lowest,
            status=_status,
            coordinate=_coordinate,
        )

    # _order = IotOrder.objects.create(
    #     mac=_mac,
    #     number=_number,
    #     device=_device,
    #     express=_express,
    #     start_time=start,
    #     end_time=end,
    #     high_temp=_hightemp,
    #     low_temp=_lowtemp,
    #     highest_temp=_highest,
    #     lowest_temp=_lowest,
    #     status=_status,
    #     coordinate=_coordinate,
    # )

    logger.debug("get ip addr")
    _ip_addr = get_client_ip(request)
    # > todo update ? create ?
    event = IotOrderEvent.objects.create(
        order=_order,
        type=_type,
        description=_ip_addr
    )
    # return HttpResponseMessageWithData(0, 'success', "order_id", _order.id)
    # 'status',_test_order
    return HttpResponseMessageWithData(0, 'success', "order", _order.id)


@csrf_exempt
def update(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
    else:
        return HttpResponseBadRequest('Bad Request')

    if 'order_id' in json_data:
        _order_id = json_data['order_id']
    else:
        return HttpResponseMessage(1, 'no order id in request')

    try:
        order = IotOrder.objects.get(pk=_order_id)
    except:
        return HttpResponseMessage(3, 'the order not exists')

    if 'mac' in json_data:
        _mac = json_data['mac']
        if order.mac != _mac:
            order.mac = _mac
            isChanged = True
            try:
                _device = IotDevice.objects.get(mac_addr=_mac)
            except:
                _device = None
            order.device = _device

    if 'number' in json_data:
        _number = json_data['number']
        if order.number != _number:
            order.number = _number
            isChanged = True
            try:
                _express = IotExpress.objects.get(number=_number)
            except:
                _express = None
            order.express = _express

    if 'start_time' in json_data:
        _starttime = json_data['start_time']
        try:
            print _starttime
            start = datetime.strptime(_starttime, dateFormat)
            order.start_time = start
            isChanged = True
        except:
            return HttpResponseMessage(4, 'start time not correct')

    if 'end_time' in json_data:
        _endtime = json_data['end_time']
        try:
            end = datetime.strptime(_endtime, dateFormat)
            order.end_time = end
            isChanged = True
        except:
            return HttpResponseMessage(5, 'end time not correct')

    if 'high_temp' in json_data:
        _hightemp = json_data['high_temp']
        order.high_temp = _hightemp
        isChanged = True

    if 'low_temp' in json_data:
        _lowtemp = json_data['low_temp']
        order.low_temp = _lowtemp
        isChanged = True

    '''
    if 'highest_temp' in json_data:
        _highest = json_data['highest_temp']
        order.highest_temp = _highest
        isChanged = True

    if 'lowest_temp' in json_data:
        _lowest = json_data['lowest_temp']
        order.lowest_temp = _lowest
        isChanged = True
    '''

    # set finished to done after data transfering done
    _type = 2
    if 'status' in json_data:
        _status = json_data['status']
        if order.status != _status:
            print _status
            order.status = _status
            isChanged = True
            if _status == STATUS_DONE:
                data = gethighlow(order.mac, order.start_time, order.end_time)
                _highest = data['highest']
                _lowest = data['lowest']
                order.highest_temp = _highest
                order.lowest_temp = _lowest
                _type = 3
            else:
                # STATUS_INIT, reset highest and lowest value
                _highest = NOT_VALID_TEMPERATURE
                _lowest = NOT_VALID_TEMPERATURE
                order.highest_temp = _highest
                order.lowest_temp = _lowest
                _type = 2
        if _status == STATUS_DONE:
            _type = 3
        else:
            _type = 2

    if isChanged:
        order.save()
        _ip_addr = get_client_ip(request)
        logger.debug(_ip_addr)
        event = IotOrderEvent.objects.create(
            order=order,
            type=_type,
            description=_ip_addr
        )

    return HttpResponseMessageWithData(0, 'success', "order_id", order.id)


@csrf_exempt
def get(request):
    logger.debug("order/get")
    if request.method == 'POST':
        json_data = json.loads(request.body)
    else:
        return HttpResponseBadRequest('Bad Request')

    if 'order_id' in json_data:
        _order_id = json_data['order_id']
        try:
            t = IotOrder.objects.get(pk=_order_id)
            order_dict = []
            a_order = t_to_dict(t)
            order_dict.append(a_order)
            return HttpResponseMessageWithData(0, 'success', "orders", order_dict)
        except:
            return HttpResponseMessage(4, 'the order id not exists')

    if 'mac' in json_data:
        _mac = json_data['mac']
        logger.debug("mac=" + _mac)
        '''
        try:
            _device = IotDevice.objects.get(mac_addr=_mac)
            print "express exist"
        except:
            _device = None
        '''
    else:
        _mac = None

    if 'number' in json_data:
        _number = json_data['number']
        '''
        try:
            _express = IotExpress.objects.get(number=_number)
            print "express exist"
        except:
            _express = None
        '''
    else:
        _number = None

    if 'status' in json_data:
        _status = json_data['status']
    else:
        _status = STATUS_ALL

    _device = None
    _express = None

    if _mac is not None and _number is not None:
        if _status == STATUS_INIT or _status == STATUS_DONE:
            if _device is None and _express is None:
                logger.debug("search with mac, number and status")
                order = IotOrder.objects.filter(number=_number, mac=_mac, status=_status).order_by('-start_time')
            else:
                # _device or express is not none, both device and express is not none
                if _device is None:
                    # express is not none
                    print "search with mac, express and status"
                    order = IotOrder.objects.filter(express=_express, mac=_mac, status=_status).order_by('-start_time')
                else:
                    # device is not none
                    if _express is None:
                        print "search with device and status"
                        order = IotOrder.objects.filter(device=_device, status=_status).order_by('-start_time')
                    else:
                        print "search with device, express and status"
                        order = IotOrder.objects.filter(device=_device, express=_express, status=_status).order_by(
                            '-start_time')
        else:
            if _device is None and _express is None:
                logger.debug("search with mac, number")
                order = IotOrder.objects.filter(number=_number, mac=_mac).order_by('-start_time')
            else:
                # _device or express is not none, both device and express is not none
                if _device is None:
                    # express is not none
                    logger.debug("search with mac, express")
                    order = IotOrder.objects.filter(express=_express, mac=_mac).order_by('-start_time')
                else:
                    # device is not none
                    if _express is None:
                        logger.debug("search with device")
                        order = IotOrder.objects.filter(device=_device).order_by('-start_time')
                    else:
                        print "search with device, express"
                        order = IotOrder.objects.filter(device=_device, express=_express).order_by('-start_time')
    else:
        if _mac is not None:
            if _status == STATUS_INIT or _status == STATUS_DONE:
                if _device is None:
                    logger.debug("search with mac and status")
                    order = IotOrder.objects.filter(mac=_mac, status=_status).order_by('-start_time')
                else:
                    logger.debug("search with device and status")
                    order = IotOrder.objects.filter(device=_device, status=_status).order_by('-start_time')
            else:
                if _device is None:
                    logger.debug("search with mac")
                    order = IotOrder.objects.filter(mac=_mac).order_by('-start_time')
                    logger.debug("search with mac end")
                else:
                    logger.debug("search with device")
                    order = IotOrder.objects.filter(device=_device).order_by('-start_time')
        else:
            if _number is not None:
                if _status == STATUS_INIT or _status == STATUS_DONE:
                    if _express is None:
                        print "search with number and status"
                        order = IotOrder.objects.filter(number=_number, status=_status).order_by('-start_time')
                    else:
                        print "search with express and status"
                        order = IotOrder.objects.filter(express=_express, status=_status).order_by('-start_time')
                else:
                    if _express is None:
                        print "search with number"
                        order = IotOrder.objects.filter(number=_number).order_by('-start_time')
                    else:
                        print "search with express"
                        order = IotOrder.objects.filter(express=_express).order_by('-start_time')
            else:
                return HttpResponseMessage(2, 'no order id, mac or express info in request')

    if order is not None and len(order) > 0:
        order_dict = []
        for t in order:
            a_order = t_to_dict(t)
            order_dict.append(a_order)
        return HttpResponseMessageWithData(0, 'success', "orders", order_dict)
    else:
        return HttpResponseMessage(4, 'the mac or number has no matched order')


@csrf_exempt
def time(request):
    return HttpResponseMessageWithData(0, 'success', "utc_time", datetime.strftime(datetime.utcnow(), dateFormat))


def gethighlow(_mac, _start, _end):
    _high = -200
    _low = 200
    temperatures = IotTemp.objects.filter(mac=_mac, time__lte=_end, time__gte=_start)
    if len(temperatures) > 0:
        logger.debug("find temperatures:" + str(len(temperatures)))
        for t in temperatures:
            if _high < t.temperature:
                _high = t.temperature
            if _low > t.temperature:
                _low = t.temperature
    else:
        logger.debug("no temperature found")
        _low = NOT_VALID_TEMPERATURE
    logger.debug("highest=" + str(_high))
    logger.debug("lowest=" + str(_low))
    data = {"highest": _high, "lowest": _low}
    return data


@require_http_methods(["GET"])
@csrf_exempt
def in_delivery(request):
    try:
        order_list = IotOrder.objects.filter(end_time__isnull=True)
        orders = []
        for order in order_list:
            a_order = t_to_dict(order)
            orders.append(a_order)
        return HttpResponseMessageWithData(0, 'success', "orders", orders)
    except:
        return HttpResponseMessage(2, 'Order not found.')


@require_http_methods(["GET"])
@csrf_exempt
def created_today(request):
    _start_time_str = request.GET.get('start_time')
    _end_time_str = request.GET.get('end_time')

    _start_time = datetime.strptime(_start_time_str, dateFormat)
    _end_time = datetime.strptime(_end_time_str, dateFormat)

    if _start_time > _end_time:
        return HttpResponseMessage(1, 'The start time is greater than end time.')

    try:
        order_list = IotOrder.objects.filter(start_time__gte=_start_time, start_time__lte=_end_time)
        orders = []
        for order in order_list:
            a_order = t_to_dict(order)
            orders.append(a_order)
        return HttpResponseMessageWithData(0, 'success', "orders", orders)
    except:
        return HttpResponseMessage(2, 'Order not found.')


@require_http_methods(["GET"])
@csrf_exempt
def delivered_today(request):
    _start_time_str = request.GET.get('start_time')
    _end_time_str = request.GET.get('end_time')

    _start_time = datetime.strptime(_start_time_str, dateFormat)
    _end_time = datetime.strptime(_end_time_str, dateFormat)

    if _start_time > _end_time:
        return HttpResponseMessage(1, 'The start time is greater than end time.')

    try:
        order_list = IotOrder.objects.filter(end_time__gte=_start_time, end_time__lte=_end_time)
        orders = []
        for order in order_list:
            a_order = t_to_dict(order)
            orders.append(a_order)
        return HttpResponseMessageWithData(0, 'success', "orders", orders)
    except:
        return HttpResponseMessage(2, 'Order not found.')

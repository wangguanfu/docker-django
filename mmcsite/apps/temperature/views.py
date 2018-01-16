import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.shortcuts import render
from datetime import datetime, timedelta
import time
import sys
import zlib

from django.utils import timezone
import pytz

from utils.views import HttpResponseMessage, HttpResponseMessageWithData, dateFormat, logger
from temperature.models import IotTemp
from device.models import IotDevice
#from iot.views.libs.express_query import ExpressQuery
#from iot.models.express import IotExpress

#mmc APIs for express
dateFormat1 = '%Y-%m-%d %H:%M'
timeDelta = 30 * 3 * 24 * 60 * 60 * 1000 #3 months
def t_to_dict(t, compressed):
    if compressed:
        t_dict = {
            "t": str(("%.1f"%t.temperature)),
            "tm": t.time.strftime(dateFormat1),
        }
    else:
        if t.device is None:
            t_dict = {
                "temperature": t.temperature,
                "seq_no": t.seq_no,
                "time": t.time.strftime(dateFormat),
                # "time": datetime.strftime(datetime.utcnow(), dateFormat)
                "mac": t.mac,
            }
        else:
            a_temperature = {
                "temperature": t.temperature,
                "seq_no": t.seq_no,
                "time": t.time.strftime(dateFormat),
                # "time": datetime.strftime(datetime.utcnow(), dateFormat)
                "mac": t.device.mac_addr,
            }
    return t_dict


@csrf_exempt
def post(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
    else:
        return HttpResponseBadRequest('Bad Request')

    if 'mac' in json_data:
        _mac = json_data['mac']
    else:
        return HttpResponseMessage(1, 'no mac in request')

    try:
        _device = IotDevice.objects.get(mac=_mac)
    except:
        _device = None

    if 'temperatures' in json_data:
        _tempSet = json_data['temperatures']
    else:
        return HttpResponseMessage(2, 'no temperatures in request')

    j = 0
    i = 0
    templist = []
    print "upload temperature count "+str(len(_tempSet))
    time1 = datetime.utcnow()

    _startStr=''
    _endStr=''
    if (len(_tempSet)>0):
        _starStr = _tempSet[0]['time']
        _endStr = _starStr
        for _temp in _tempSet:
            if _starStr>_temp['time']:
                _starStr = _temp['time']
            if _endStr < _temp['time']:
                _endStr = _temp['time']
        _start = datetime.strptime(_starStr, dateFormat) - timedelta(days=7)
        _end = datetime.strptime(_endStr, dateFormat) + timedelta(days=7)
        # filter out all the temp in scope
        _temps = IotTemp.objects.filter(mac=_mac, time__lte=_end, time__gte=_start)
        #print "found temps count"+ str(len(_temps))
        print _start
        print _end
        _temp_set = set() #add the seq_no to set
        for _a in _temps:
            _temp_set.add(_a.seq_no)
        for _temp in _tempSet:
            if _temp['seq_no'] not in _temp_set:
                # the temperature to be added to db
                templist.append(IotTemp(mac=_mac, device=_device, temperature=_temp['temperature'], seq_no=_temp['seq_no'],
                            time=datetime.strptime(_temp['time'], dateFormat), description=""))
                j=j+1
            else:
                i=i+1
        _temp_set.clear()

    time2 = datetime.utcnow()
    print "time for data query:"+str(time2-time1)
    if len(templist)>0:
        print "insert temperature count "+str(len(templist))
        try:
            IotTemp.objects.bulk_create(templist)
            time3 = datetime.utcnow()
            print "time for insert temperature:"+str(time3-time1)
            return HttpResponseMessageWithData(0, 'success', 'add', j)
        except:
            return HttpResponseMessage(3, 'duplicated index in input')
    else:
        return HttpResponseMessageWithData(0, 'success', 'duplicated', i)

@csrf_exempt
def get(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
    else:
        return HttpResponseBadRequest('Bad Request')

    if 'mac' in json_data:
        _mac = json_data['mac']
    else:
        return HttpResponseMessage(1, 'no mac in request')

    if 'start_time' in json_data:
        _starttime = json_data['start_time']
        try:
            start = datetime.strptime(_starttime, dateFormat)
        except:
            return HttpResponseMessage(4, 'start time not correct')
    else:
        return HttpResponseMessage(2, 'no start time in request')

    if 'end_time' in json_data:
        _endtime = json_data['end_time']
        try:
            end = datetime.strptime(_endtime, dateFormat)
        except:
            return HttpResponseMessage(5, 'end time not correct')
    else:
        return HttpResponseMessage(3, 'no end time in request')

    time1 = datetime.utcnow()
    temperatures = IotTemp.objects.filter(mac=_mac, time__lte=end, time__gte=start).order_by('seq_no')
    time2 = datetime.utcnow()
    if len(temperatures) > 0:
        print "find temperature count "+ str(len(temperatures))
        temp_dict = []
        for t in temperatures:
            temp_dict.append(t_to_dict(t, False))
        time3 = datetime.utcnow()
        logger.debug("time for getting temperature:"+ str(time3 - time1))
        print "temp_dict size:"+str(len(json.dumps(temp_dict)))
        return HttpResponseMessageWithData(0, 'success', 'temperatures', temp_dict)
    else:
        #result = {"start_str": _starttime, "start": datetime.strftime(start, dateFormat), "end_str": _endtime, "end": datetime.strftime(end, dateFormat)}
        #return HttpResponseMessageWithData(3, 'no temperature data', 'time', json.dumps(result))
        return HttpResponseMessage(6, 'no temperature data')

@csrf_exempt
def get_seq(request):
    _mac = request.GET.get('mac')
    print _mac
    if _mac is None:
        return HttpResponseMessage(1, 'no mac provided')
    # only check temperatures posted in 3 months
    #start = datetime.utcnow() - timeDelta
    _device = IotDevice.objects.filter(mac_addr=_mac)
    if len(_device)>0:
        temp = IotTemp.objects.filter(device=_device[0]).order_by('-seq_no')[0]
    else:
        print "no device info"
        temp = IotTemp.objects.filter(mac=_mac).order_by('-seq_no')[0]
    if temp is not None:
        return HttpResponseMessageWithData(0, "success", "seq_no", temp.seq_no)



@csrf_exempt
def get_compressed(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
    else:
        return HttpResponseBadRequest('Bad Request')

    if 'mac' in json_data:
        _mac = json_data['mac']
    else:
        return HttpResponseMessage(1, 'no mac in request')

    if 'start_time' in json_data:
        _starttime = json_data['start_time']
        try:
            start = datetime.strptime(_starttime, dateFormat)
        except:
            return HttpResponseMessage(4, 'start time not correct')
    else:
        return HttpResponseMessage(2, 'no start time in request')

    if 'end_time' in json_data:
        _endtime = json_data['end_time']
        try:
            end = datetime.strptime(_endtime, dateFormat)
        except:
            return HttpResponseMessage(5, 'end time not correct')
    else:
        return HttpResponseMessage(3, 'no end time in request')

    if 'compressed' in json_data:
        _compressed = True
    else:
        _compressed = False

    _compressed = True
    #IotTemp.objects.get(time.c)
    #temperatures = IotTemp.objects.filter(mac = _mac, time=end, time__gte=start)
    time1 = datetime.utcnow()
    temperatures = IotTemp.objects.filter(mac=_mac, time__lte=end, time__gte=start).order_by('seq_no')
    time2 = datetime.utcnow()
    if len(temperatures) > 0:
        print "find temperature count "+ str(len(temperatures))
        temp_dict = []
        for t in temperatures:
            temp_dict.append(t_to_dict(t, _compressed))
        time3 = datetime.utcnow()
        logger.debug("time for getting temperature:"+ str(time3 - time1))
        #str1 = zlib.compress(json.dumps(dict1), zlib.Z_BEST_COMPRESSION)
        return HttpResponseMessageWithCompressedData(0, 'success', 'temperatures', temp_dict)
        #return HttpResponse(str1, content_type = 'application/json')
    else:
        #result = {"start_str": _starttime, "start": datetime.strftime(start, dateFormat), "end_str": _endtime, "end": datetime.strftime(end, dateFormat)}
        #return HttpResponseMessageWithData(3, 'no temperature data', 'time', json.dumps(result))
        return HttpResponseMessage(6, 'no temperature data')


def HttpResponseMessageWithCompressedData(result, message, data_key, data):
    dict = {
        "result": result,
        "message": message,
        data_key: data
        }
    return HttpResponse(json.dumps(dict, separators=(',',':')), content_type = 'application/json')

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
    else:
        return HttpResponseBadRequest('Bad Request')

    _starttime = ''
    _endtime = ''
    if 'mac' in json_data:
        _mac = json_data['mac']
    else:
        return HttpResponseMessage(1, 'no mac in request')

    temps = IotTemp.objects.filter(mac=_mac)

    if (len(temps)>0):
        print len(temps)
        num = temps.delete()
    else:
        num = 0

    return HttpResponseMessageWithCompressedData(0, 'success', 'delete temperature count', num)

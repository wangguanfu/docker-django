# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.http import HttpResponse
import logging

# utils
dateFormat = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger('iot')


def HttpResponseMessage(result, message):
    dict = {
        "result": result,
        "message": message
    }
    return HttpResponse(json.dumps(dict), content_type='application/json')


def HttpResponseMessageWithData(result, message, data_key, data):
    dict = {
        "result": result,
        "message": message,
        data_key: data
    }
    return HttpResponse(json.dumps(dict), content_type='application/json')

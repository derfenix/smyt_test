# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import json
import decimal
from django.db.models.base import ModelState


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'strftime'):
            return obj.strftime('%d-%m-%Y')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, ModelState):
            return None
        else:
            return json.JSONEncoder.default(self, obj)
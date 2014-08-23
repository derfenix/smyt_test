# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import datetime
from django import template
from django.utils import dateformat
from django.conf import settings


register = template.Library()


@register.simple_tag
def get_field(obj, f):
    val = getattr(obj, f, '')
    if isinstance(val, datetime.date):
        val = dateformat.format(val, settings.DATE_FORMAT)
    return val
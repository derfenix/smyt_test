# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, unicode_literals
from collections import OrderedDict
import json

from django.db.models.loading import get_model
from django.http.response import Http404, HttpResponse
from django.views.generic.base import TemplateView, ContextMixin, View

from main.utils import DateTimeEncoder
from .models import MODELS_DATA


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['models'] = json.dumps(MODELS_DATA)
        context['pymodels'] = MODELS_DATA
        return context


class MainView(ContextMixin, View):
    http_method_names = ('get', 'post')
    template_name = 'index.html'
    model_name = None
    """:type: str or unicode"""
    _fields_types = {}
    object = None

    @staticmethod
    def render_to_response(context, **response_kwargs):
        return HttpResponse(
            json.dumps(context, ensure_ascii=False, cls=DateTimeEncoder, indent=4),
            content_type="application/json"
        )

    def dispatch(self, request, *args, **kwargs):
        self.model_name = kwargs.get('model', None)
        """:type: str or unicode"""
        if self.model_name is None or self.model_name not in MODELS_DATA:
            raise Http404(self.model_name)
        return super(MainView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'entires': list(self.model.objects.all().values()),
            'model_name': self.model_name,
        }
        return context

    @property
    def model(self):
        """Model class"""
        return get_model('main', self.model_name)

    @classmethod
    def fields_types(cls, model_name):
        """Transform MODELS_DATA into dict {field_name: field_type} with caching

        :param model_name: name of model
        :type model_name: str or unicode
        :return: dict {field_name: field_type}
        :rtype: dict
        """
        if model_name not in cls._fields_types:
            fields = MODELS_DATA.get(model_name).get('fields')
            fields = OrderedDict(((i['id'], i['type']) for i in fields))
            cls._fields_types[model_name] = fields
        return cls._fields_types[model_name]

    def test_value(self, field, value):
        """Test if value is in format, that valid for specified field

        :param field: field name
        :type field: str
        :param value: value for test
        :type value: str or unicode
        :return: value
        :rtype: int or unicode or datetime.datetime
        """
        field_type = self.fields_types(self.model_name)[field]
        val = False

        try:
            if field_type == 'int':
                val = int(value)
            elif field_type == 'char':
                val = unicode(value)
            elif field_type == 'date':
                import datetime

                val = datetime.datetime.strptime(value, '%d-%m-%Y')
        except (ValueError, TypeError):
            return None

        return val

    def update_value(self, data):
        """Update model's record

        :param data: post data
        :type data: dict
        :return: error message if any
        :rtype: unicode
        """
        item_id = int(data.get('id', 0))
        """:type: int"""
        if not item_id:
            return "No id specified"

        field = data.get('field', None)
        """:type: str or unicode"""
        if not field:
            return "No field specified"

        value = data.get('value', None)
        """:type: str or unicode"""
        value = self.test_value(field, value)
        if not value:
            return "Value is in wrong format"

        if not self.model.objects.filter(id=item_id).exists():
            return "Wrong id"

        item = self.model.objects.get(id=item_id)
        """:type: django.db.models.Model"""

        try:
            setattr(item, field, value)
        except AttributeError:
            return "Wrong field name"
        except ValueError:
            return "Wrong value"
        else:
            item.save(update_fields=(field,))

        return None

    def save_form(self, data):
        """Save form data

        :param data: POST data
        :type data: dict
        :return: dict with errors and values
        :rtype: dict[dict]
        """
        item = self.model()
        """:type: django.db.models.Model"""
        errors = {}

        for name, ftype in self.fields_types(self.model_name).items():
            value = data.get(name, None)
            """:type: str or unicode"""
            new_value = self.test_value(name, value)

            if not value:
                errors[name] = 'Value is required'
            elif not new_value:
                errors[name] = 'Value is in wrong format'
            else:
                if not errors:
                    # If errors already exists - no need to set
                    setattr(item, name, new_value)

        if not errors:
            item.save(force_insert=True)
        else:
            return {
                'errors': errors,
                'values': data
            }

    def post(self, request, *args, **kwargs):
        if request.POST.get('new', False):
            res = self.save_form(request.POST)
            context = self.get_context_data()

            if res:  # Errors exists
                # Append errors and values lists to context
                context.update(res)
            # If no errorrs - just return standart context - entries list and form fields

            return self.render_to_response(context)
        else:
            res = self.update_value(request.POST)
            if res:
                res = {'status': 'error', 'message': res}
            else:
                res = {'status': 'OK'}
            return self.render_to_response(res)

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())
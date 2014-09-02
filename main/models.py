from __future__ import print_function, absolute_import, unicode_literals
from django.contrib import admin
from django.db import models
from django.conf import settings
import yaml

# Models already builded
BUILDED = False
""":type: bool"""

# Models specifications loaded from file
MODELS_DATA = None
""":type: dict"""


class Builder(object):
    """
    Models builder class
    """

    def __init__(self, filepath=None):
        """
        :param filepath: path to models' specifications file
        :type filepath: str or unicode
        """
        self.models = {}
        self.models_data = None
        self.filepath = filepath

    @staticmethod
    def __build_meta(title):
        """Build Meta-class for model

        :param title: models verbose name
        :type title: str or unicode
        :return: Meta-class
        :rtype: type
        """

        class Meta:
            pass

        setattr(Meta, 'app_label', 'main')
        setattr(Meta, 'verbose_name', title)
        setattr(Meta, 'verbose_name_plural', title)
        return Meta

    def __load(self):
        """Load models' specifications from file
        """
        with open(self.filepath, 'r') as f:
            filedata = f.read()

        self.models_data = yaml.load(filedata)

    @staticmethod
    def __get_field(field_type, params):
        """Get field instance

        :param field_type: field type
        :type field_type: str
        :param params: field params
        :type params: dict
        :return: Field instance
        :rtype: django.db.models.fields.Field
        """
        verbose_name = params.get('title', None)

        if field_type == 'char':
            return models.CharField(
                max_length=255, verbose_name=verbose_name
            )
        elif field_type == 'int':
            return models.IntegerField(verbose_name=verbose_name)
        elif field_type == 'date':
            return models.DateField(verbose_name=verbose_name)

    def build(self):
        """Build models' classes, store them into self.models and
        register admin interfaces for this models
        """
        self.__load()

        for name, data in self.models_data.items():
            attrs = {
                params['id']: self.__get_field(params.get('type', 'char'), params)
                for params in data['fields']
            }

            attrs['__module__'] = 'main.models'
            attrs['Meta'] = self.__build_meta(data.get('title', None))
            attrs['__unicode__'] = lambda s: "{0} #{1}".format(name, s.id)

            model = type(name, (models.Model,), attrs)
            self.models[name.title()] = model
            admin.site.register(model)

    @property
    def result(self):
        """Get dict for update module's locals

        :return: builded models
        :rtype: dict
        """
        result = self.models
        result['MODELS_DATA'] = self.models_data
        return result


if not BUILDED:
    # Build models
    builder = Builder(getattr(settings, 'MODELS_DEFENITION_FILE_PATH', None))
    builder.build()

    # Update module's locals
    locals().update(builder.result)

    BUILDED = True
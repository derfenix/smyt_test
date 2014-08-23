# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import os

from django.test.runner import DiscoverRunner
from django.conf import settings


class TestRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        settings.MODELS_DEFENITION_FILE_PATH = os.path.join(
            settings.BASE_DIR, 'main', 'tests', 'models.yaml'
        )
        super(TestRunner, self).setup_test_environment(**kwargs)

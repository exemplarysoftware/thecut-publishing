# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import VERSION as DJANGO_VERSION

if DJANGO_VERSION < (1, 6):
    from .test_models import *  # NOQA
    from .test_querysets import *  # NOQA

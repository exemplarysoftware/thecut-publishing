# coding=utf-8
from __future__ import absolute_import, unicode_literals
from django.contrib import admin


def enable(model_admin, request, queryset):
    """'Enable' every object in the queryset."""
    queryset.update(is_enabled=True)

enable.short_description = 'Enable items'


def feature(model_admin, request, queryset):
    """'Feature' every object in the queryset."""
    queryset.update(is_featured=True)

feature.short_description = 'Feature items'

# coding=utf-8
from __future__ import absolute_import, unicode_literals
from django.contrib import messages
from django.core.exceptions import FieldDoesNotExist


def enable(model_admin, request, queryset):
    """'Enable' every object in the queryset."""
    try:
        queryset.update(is_enabled=True)
    except FieldDoesNotExist:
        msg = "Some of the items you selected could not be enabled."
        model_admin.message_user(request, msg, level=messages.ERROR)
    else:
        msg = "The selected items were enabled successfully."
        model_admin.message_user(request, msg, level=messages.SUCCESS)

enable.short_description = 'Enable items'


def feature(model_admin, request, queryset):
    """'Feature' every object in the queryset."""
    try:
        queryset.update(is_featured=True)
    except FieldDoesNotExist:
        msg = "Some of the items you selected could not be featured."
        model_admin.message_user(request, msg, level=messages.ERROR)
    else:
        msg = "The selected items were featured successfully."
        model_admin.message_user(request, msg, level=messages.SUCCESS)

feature.short_description = 'Feature items'

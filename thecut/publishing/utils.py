# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.core.exceptions import ObjectDoesNotExist

try:
    from django.utils.text import slugify
except ImportError:
    # Pre-Django 1.5
    from django.template.defaultfilters import slugify


def generate_unique_slug(text, queryset, slug_field='slug', iteration=0):
    """Generate a unique slug for a model from the provided text."""
    slug = slugify(text)

    if iteration > 0:
        slug = '{0}-{1}'.format(iteration, slug)
    slug = slug[:50]

    try:
        queryset.get(**{slug_field: slug})
    except ObjectDoesNotExist:
        return slug
    else:
        iteration += 1
        return generate_unique_slug(text, queryset=queryset,
                                    slug_field=slug_field, iteration=iteration)


def python_2_unicode_compatible(class_):
    # Forwards compatibility with Django 1.5, taken from Django 1.4.5
    class_.__unicode__ = class_.__str__
    class_.__str__ = lambda self: self.__unicode__().encode('utf-8')
    return class_

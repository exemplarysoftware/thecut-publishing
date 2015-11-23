# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from ..utils import generate_unique_slug
from django.test import TestCase
from test_app.factories import ConcreteSiteContentWithSlugFactory
from test_app.models import ConcreteSiteContentWithSlug

class TestGenerateUniqueSlug(TestCase):

    """Test for utils.generate_unique_slug()"""

    # TODO: Mocking

    def setUp(self):
        self.c1 = ConcreteSiteContentWithSlugFactory(title='Content A')
        self.c2 = ConcreteSiteContentWithSlugFactory(title='Content B')

    def test_generates_slug_with_unique_slugified_text(self):
        queryset = ConcreteSiteContentWithSlug.objects.all()
        self.c1.title = 'A unique title'
        slug = generate_unique_slug(self.c1.title, queryset)
        self.assertEqual(slug, 'a-unique-title')

    def test_generates_slug_without_unique_slugified_text(self):
        queryset = ConcreteSiteContentWithSlug.objects.all()
        self.c1.title = 'Content B'
        slug = generate_unique_slug(self.c1.title, queryset)
        self.assertEqual(slug, '1-content-b')

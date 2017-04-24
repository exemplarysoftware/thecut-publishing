# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from ..utils import generate_unique_slug
from django.test import TestCase
from test_app.factories import ConcreteSiteContentWithSlugFactory
from test_app.models import ConcreteSiteContentWithSlug


class TestGenerateUniqueSlug(TestCase):

    """Test for utils.generate_unique_slug()"""

    def setUp(self):
        self.content = ConcreteSiteContentWithSlugFactory(slug='blah')

    def test_generates_unique_slug_from_unique_text(self):
        """Test if a unique slug is generated from a unique string."""
        queryset = ConcreteSiteContentWithSlug.objects.all()
        slug = generate_unique_slug(text=self.content.slug[::-1],
                                    queryset=queryset)
        self.assertFalse(ConcreteSiteContentWithSlug.objects.filter(slug=slug))

    def test_generates_unique_slug_from_common_text(self):
        """Test if a unique slug is generated from a common string."""
        queryset = ConcreteSiteContentWithSlug.objects.all()
        slug = generate_unique_slug(text=self.content.slug,
                                    queryset=queryset)
        self.assertFalse(ConcreteSiteContentWithSlug.objects.filter(slug=slug))
        self.assertEqual(slug, '1-blah')

    def test_generates_unique_slug_from_empty_string(self):
        """Test if a slug is generated from an empty string."""
        queryset = ConcreteSiteContentWithSlug.objects.all()
        slug = generate_unique_slug(text='',
                                    queryset=queryset)
        self.assertFalse(ConcreteSiteContentWithSlug.objects.filter(slug=slug))

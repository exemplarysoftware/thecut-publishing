# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from freezegun import freeze_time
from mock import Mock
from test_app.models import (
    ConcreteContent, ConcreteContentFactory, ConcretePublishableResource,
    ConcretePublishableResourceFactory)


class TestPublishableResourceQuerySetFeatured(TestCase):

    def test_includes_instance_with_is_featured_true(self):
        featured = ConcretePublishableResourceFactory(is_featured=True)

        queryset = ConcretePublishableResource.objects.featured()

        self.assertIn(featured, queryset)

    def test_excludes_instance_with_is_featured_false(self):
        not_featured = ConcretePublishableResourceFactory(is_featured=False)

        queryset = ConcretePublishableResource.objects.featured()

        self.assertNotIn(not_featured, queryset)


class TestPublishableResourceQuerySetActive(TestCase):

    def test_excludes_instance_with_published_at_in_the_future(self):
        later = timezone.now() + timedelta(days=1)
        inactive = ConcretePublishableResourceFactory(publish_at=later)

        queryset = ConcretePublishableResource.objects.active()

        self.assertNotIn(inactive, queryset)

    def test_includes_instance_with_published_at_in_the_past(self):
        earlier = timezone.now() - timedelta(days=1)
        active = ConcretePublishableResourceFactory(publish_at=earlier)

        queryset = ConcretePublishableResource.objects.active()

        self.assertIn(active, queryset)

    def test_includes_instance_with_published_at_now(self):
        now = timezone.now()
        active = ConcretePublishableResourceFactory(publish_at=now)

        with freeze_time(now):
            queryset = ConcretePublishableResource.objects.active()

        self.assertIn(active, queryset)


class TestContentQuerySetIndexable(TestCase):

    def test_includes_content_with_is_indexable_true(self):
        indexable = ConcreteContentFactory(is_indexable=True)

        queryset = ConcreteContent.objects.indexable()

        self.assertIn(indexable, queryset)

    def test_excludes_content_with_is_indexable_false(self):
        unindexable = ConcreteContentFactory(is_indexable=False)

        queryset = ConcreteContent.objects.indexable()

        self.assertNotIn(unindexable, queryset)

    def test_calls_active_on_self(self):
        # Ensure we're also filtering inactive content out of the results when
        # finding indexable content.
        indexable = ConcreteContentFactory(is_indexable=True)
        ConcreteContent.objects.active = Mock()

        queryset = ConcreteContent.objects.indexable()

        self.assertTrue(ConcreteContent.objects.active.called_once)

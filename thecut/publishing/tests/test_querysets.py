# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from freezegun import freeze_time
from test_app.models import ConcretePublishableResource, ConcretePublishableResourceFactory


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

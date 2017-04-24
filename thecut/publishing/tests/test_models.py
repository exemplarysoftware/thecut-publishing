# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.test import TestCase, TransactionTestCase
from mock import patch
from thecut.publishing import utils
from test_app.factories import (ConcreteContentFactory,
                                ConcretePublishableResourceFactory,
                                ConcreteSiteContentWithSlugFactory,
                                ConcreteSiteContentFactory)
from test_app.models import (ConcretePublishableResource,
                             ConcreteSiteContentWithSlug)
from django.utils import timezone
from datetime import timedelta
from freezegun import freeze_time


class TestPublishableResource(TestCase):

    def test_gets_latest_by_publish_at(self):
        older = ConcretePublishableResourceFactory()
        newer = ConcretePublishableResourceFactory()

        latest = ConcretePublishableResource.objects.latest()

        self.assertGreater(newer.publish_at, older.publish_at)
        self.assertEqual(latest, newer)


class TestContentHeading(TestCase):

    def test_returns_headline_if_headline_is_set(self):
        content = ConcreteContentFactory(headline='headline')

        self.assertEqual(content.heading, content.headline)

    def test_returns_title_if_headline_is_not_set(self):
        content = ConcreteContentFactory(title='title', headline='')

        self.assertEqual(content.heading, content.title)


class TestSiteContentWithSlug(TestCase):

    def test_sets_slug_if_slug_is_unset_on_save(self):
        content = ConcreteSiteContentWithSlugFactory(slug=None)

        self.assertIsNotNone(content.slug)
        self.assertGreater(len(content.slug), 0)

    def test_does_not_overwrite_slug_if_a_slug_is_set(self):
        content = ConcreteSiteContentWithSlugFactory(slug='a-slug')

        self.assertEqual(content.slug, 'a-slug')

    @patch('thecut.publishing.utils.generate_unique_slug')
    def test_generates_unique_slug_for_content_title_and_site(self, mock_generate_unique_slug):  # NOQA
        mock_generate_unique_slug.return_value = 'a-slug'

        content = ConcreteSiteContentWithSlugFactory(slug=None)
        queryset = ConcreteSiteContentWithSlug.objects.filter(
            site=content.site)

        self.assertTrue(utils.generate_unique_slug.called_once_with(
            content.title, queryset))


class TestGetCurrentSite(TransactionTestCase):
    def test_site_content_creation(self):
        ConcreteSiteContentFactory()


class TestPublishableResourceModelActive(TestCase):

    def test_excludes_instance_with_published_at_in_the_future(self):
        later = timezone.now() + timedelta(days=1)
        inactive = ConcretePublishableResourceFactory(publish_at=later)

        self.assertFalse(inactive.is_active())

    def test_includes_instance_with_published_at_in_the_past(self):
        earlier = timezone.now() - timedelta(days=1)
        active = ConcretePublishableResourceFactory(publish_at=earlier)

        self.assertTrue(active.is_active())

    def test_includes_instance_with_published_at_now(self):
        now = timezone.now()
        active = ConcretePublishableResourceFactory(publish_at=now)

        with freeze_time(now):
            self.assertTrue(active.is_active())

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.sites.models import Site
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from freezegun import freeze_time
from mock import Mock
from test_app.factories import (ConcreteContentFactory,
                                ConcretePublishableResourceFactory,
                                ConcreteSiteContentFactory, SiteFactory)
from test_app.models import (ConcreteContent, ConcretePublishableResource,
                             ConcreteSiteContent)


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

    def test_excludes_inactive_content(self):
        # This isn't a very extensive test. The fact that disabled content
        # is being filtered is not proof that all inactive content is being
        # filtered
        disabled = ConcreteContentFactory(is_enabled=False)
        queryset = ConcreteContent.objects.indexable()

        self.assertNotIn(disabled, queryset)


class TestSiteContentQuerySetCurrentSite(TestCase):

    def test_includes_content_whose_site_matches_the_current_site(self):
        content = ConcreteSiteContentFactory()
        Site.objects.get_current = Mock(return_value=content.site)

        queryset = ConcreteSiteContent.objects.current_site()

        self.assertIn(content, queryset)

    def test_excludes_content_whose_site_does_not_match_the_current_site(self):
        content = ConcreteSiteContentFactory()
        # Pretend our site content belongs to a different site than the current
        # one.
        another_site = SiteFactory(name='a different site')
        Site.objects.get_current = Mock(return_value=another_site)

        queryset = ConcreteSiteContent.objects.current_site()

        self.assertNotIn(content, queryset)

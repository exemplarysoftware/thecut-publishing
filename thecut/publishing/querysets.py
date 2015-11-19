# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone


class PublishableResourceQuerySet(models.query.QuerySet):
    """Customised :py:class:`~django.db.models.db.query.QuerySet` for
    :py:class:`~thecut.publishing.models.PublishableResource` model."""

    def active(self):
        """Filter for objects which are active (enabled, published).

        :returns: Filtered queryset.
        :rtype: :py:class:`.PublishableResourceQuerySet`
        """
        now = timezone.now()
        return self.filter(is_enabled=True).filter(
            models.Q(publish_at__lte=now),
            models.Q(expire_at__isnull=True) | models.Q(expire_at__gte=now))

    def inactive(self):
        """Filter for objects wich are inactive.

        An object is inactive if it is either:
        - Not enabled
        - Expired
        - Not yet published (published in the future)

        :returns: Filtered queryset.
        :rtype: :py:class:`.PublishableResourceQuerySet`
        """
        now = timezone.now()
        return self.filter(
            models.Q(is_enabled=False) |
            models.Q(publish_at__gt=now) |
            models.Q(expire_at__lte=now)
        )

    def featured(self):
        """Filter for objects which are featured.

        :returns: Filtered queryset.
        :rtype: :py:class:`.PublishableResourceQuerySet`

        """
        return self.filter(is_featured=True)


class ContentQuerySet(PublishableResourceQuerySet):
    """Customised :py:class:`~django.db.models.db.query.QuerySet` for
    :py:class:`~thecut.publishing.models.ContentQuerySet` model."""

    def indexable(self):
        """Filter for objects which are indexable.

        :returns: Filtered queryset.
        :rtype: :py:class:`.ContentQuerySet`

        """
        return self.filter(is_indexable=True).active()


class SiteContentQuerySet(ContentQuerySet):
    """Customised :py:class:`~django.db.models.db.query.QuerySet` for
    :py:class:`~thecut.publishing.models.SiteContentQuerySet` model."""

    def current_site(self):
        """Filter for objects for the current site.

        :returns: Filtered queryset.
        :rtype: :py:class:`.SiteContentQuerySet`

        """
        site = Site.objects.get_current()
        return self.filter(site=site)

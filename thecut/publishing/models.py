# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from model_utils.managers import PassThroughManager
from taggit.managers import TaggableManager
from thecut.authorship.models import Authorship
from thecut.publishing import settings, querysets, utils


def get_current_site():
    try:
        return Site.objects.get_current().pk
    except Site.DoesNotExist:
        pass


class PublishableResource(Authorship):
    """Abstract resource model with publishing related fields.

    """

    is_enabled = models.BooleanField('enabled', db_index=True, default=True)
    is_featured = models.BooleanField('featured', db_index=True, default=False)

    publish_at = models.DateTimeField(
        'publish date & time',
        db_index=True,
        default=timezone.now,
        help_text='This item will only be viewable on the website if it is '
                  'enabled, and this date and time has past.')
    expire_at = models.DateTimeField(
        'expiry date & time',
        db_index=True,
        null=True,
        blank=True,
        help_text='This item will no longer be viewable on the website if '
                  'this date and time has past. Leave blank if you do not '
                  'wish this item to expire.')

    publish_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                   blank=True, related_name='+')

    objects = PassThroughManager().for_queryset_class(
        querysets.PublishableResourceQuerySet)()

    class Meta(object):
        abstract = True
        get_latest_by = 'publish_at'

    def is_active(self):
        return self in self.__class__.objects.filter(pk=self.pk).active()


@python_2_unicode_compatible
class Content(PublishableResource):
    """Abstract model with publishing and content fields.

    """

    title = models.CharField(max_length=200)
    headline = models.CharField(max_length=200, blank=True, default='')
    content = models.TextField(blank=True, default='')
    featured_content = models.TextField(blank=True, default='')
    tags = TaggableManager(blank=True, related_name='+')

    is_indexable = models.BooleanField(
        'indexable',
        db_index=True,
        default=True,
        help_text='Should this page be indexed by search engines?')

    meta_description = models.CharField(
        max_length=200,
        blank=True,
        default='',
        help_text='Optional short description for use by search engines.')

    template = models.CharField(max_length=100, blank=True, default='',
                                help_text='Example: "app/model_detail.html".')

    objects = PassThroughManager().for_queryset_class(
        querysets.ContentQuerySet)()

    class Meta(PublishableResource.Meta):
        abstract = True
        ordering = ('title',)

    def __str__(self):
        return self.title

    @property
    def heading(self):
        return self.headline if self.headline else self.title


class SiteContent(Content):
    """Abstract model with publishing and content fields, related to a site.

    """

    site = models.ForeignKey('sites.Site', default=get_current_site)

    objects = PassThroughManager().for_queryset_class(
        querysets.SiteContentQuerySet)()

    class Meta(Content.Meta):
        abstract = True


class SiteContentWithSlug(SiteContent):
    """Abstract model with publishing, content, and slug fields - related to a
    site.

    """

    slug = models.SlugField()

    class Meta(SiteContent.Meta):
        abstract = True
        unique_together = ('site', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            queryset = self.__class__.objects.filter(site=self.site)
            self.slug = utils.generate_unique_slug(self.title, queryset)
        return super(SiteContentWithSlug, self).save(*args, **kwargs)

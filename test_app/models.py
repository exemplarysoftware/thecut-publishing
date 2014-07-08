# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.sites.models import Site
import factory
from thecut.authorship.factories import AuthorshipFactory
from thecut.publishing.models import Content, PublishableResource, SiteContent
from thecut.publishing.factories import ContentFactory


class ConcretePublishableResource(PublishableResource):

    pass


class ConcretePublishableResourceFactory(AuthorshipFactory):

    class Meta(object):
        model = ConcretePublishableResource


class ConcreteContent(Content):

    pass


class ConcreteContentFactory(ContentFactory):

    class Meta(object):
        model = ConcreteContent


class ConcreteSiteContent(SiteContent):

    pass


class SiteFactory(factory.DjangoModelFactory):

    name = factory.Sequence(lambda n: 'Site {0}'.format(n))
    domain = factory.Sequence(lambda n: 'www.site{0}.com'.format(n))

    class Meta(object):
        model = Site
        django_get_or_create = ('name',)


class ConcreteSiteContentFactory(ConcreteContentFactory):

    site = factory.SubFactory(SiteFactory)

    class Meta(object):
        model = ConcreteSiteContent

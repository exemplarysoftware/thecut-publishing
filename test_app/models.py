# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from thecut.authorship.factories import AuthorshipFactory
from thecut.publishing.models import Content, PublishableResource
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

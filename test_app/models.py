# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from thecut.publishing.models import PublishableResource
from thecut.authorship.factories import AuthorshipFactory


class ConcretePublishableResource(PublishableResource):

    pass


class ConcretePublishableResourceFactory(AuthorshipFactory):

    class Meta(object):
        model = ConcretePublishableResource

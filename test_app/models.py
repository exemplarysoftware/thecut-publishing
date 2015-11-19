# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from thecut.publishing.models import (
    Content, PublishableResource, SiteContent, SiteContentWithSlug)


class ConcretePublishableResource(PublishableResource):

    pass


class ConcreteContent(Content):

    pass


class ConcreteSiteContent(SiteContent):

    pass


class ConcreteSiteContentWithSlug(SiteContentWithSlug):

    pass

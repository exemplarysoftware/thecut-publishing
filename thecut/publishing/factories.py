# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from thecut.authorship.factories import AuthorshipFactory
import random

try:
    from faker import Factory as FakerFactory
except ImportError as error:
    message = '{0}. Try running `pip install faker`.'.format(error)
    raise ImportError(message)

try:
    import factory
except ImportError as error:
    message = '{0}. Try running `pip install factory_boy`.'.format(error)
    raise ImportError(message)


faker = FakerFactory.create()


class ContentFactory(AuthorshipFactory):

    class Meta(object):
        abstract = True

    title = factory.Sequence(lambda n: 'Content {0}'.format(n))


def _generate_list_items(quantity):
    return ['<li>{0}</li>'.format(sentence)
            for sentence in faker.sentences(quantity)]


def _generate_ol(item_quantity):
    return '<ol>{0}</ol>'.format(
        ''.join(_generate_list_items(item_quantity)))


def _generate_paragraphs(quantity):
    return ['<p>{0}</p>'.format(paragraph)
            for paragraph in faker.paragraphs(quantity)]


def _generate_ul(item_quantity):
    return '<ul>{0}</ul>'.format(
        ''.join(_generate_list_items(item_quantity)))


class ContentFakerFactory(ContentFactory):

    class Meta(object):
        abstract = True

    title = factory.LazyAttribute(lambda o: faker.company())

    headline = factory.LazyAttribute(lambda o: faker.catch_phrase())

    featured_content = factory.LazyAttribute(lambda o: faker.paragraph())

    meta_description = factory.LazyAttribute(lambda o: faker.sentence())

    created_by = factory.SubFactory(
        'thecut.authorship.factories.UserFakerFactory')

    @factory.lazy_attribute
    def content(self):
        paragraphs = _generate_paragraphs(random.randint(5, 20))
        ul = _generate_ul(6)
        ol = _generate_ol(4)
        h2 = '<h2>{0}</h2>'.format(faker.catch_phrase())
        h3 = '<h3>{0}</h3>'.format(faker.city())
        return paragraphs[0] + h2 + paragraphs[1] + ul + paragraphs[2] + \
            paragraphs[3] + h3 + ol + ''.join(paragraphs[4:])

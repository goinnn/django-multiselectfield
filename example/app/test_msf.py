# -*- coding: utf-8 -*-
# Copyright (c) 2013 by Pablo Martín <goinnn@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import sys

from django import VERSION
from django.core.exceptions import ValidationError
from django.forms.models import modelform_factory
from django.test import TestCase

from multiselectfield.utils import get_max_length

from .models import Book, PROVINCES, STATES, PROVINCES_AND_STATES


if sys.version_info < (3,):
    u = unicode  # noqa: F821
else:
    u = str


if VERSION < (1, 9):
    def get_field(model, name):
        return model._meta.get_field_by_name(name)[0]
else:
    def get_field(model, name):
        return model._meta.get_field(name)


class MultiSelectTestCase(TestCase):

    fixtures = ['app_data.json']
    maxDiff = 4000

    def assertListEqual(self, left, right, msg=None):
        if sys.version_info >= (3, 2):
            # Added in Python 3.2
            self.assertCountEqual(left, right, msg=msg)
        else:
            # Manually check list equality
            self.assertEqual(len(left), len(right), msg=msg)
            for i, tag_list in enumerate(left):
                for j, tag in enumerate(tag_list):
                    self.assertEqual(tag, right[i][j], msg=msg)

    def assertStringEqual(self, left, right, msg=None):
        _msg = "Chars in position %%d differ: %%s != %%s. %s" % msg

        # Compare characters individually
        for i, chars in enumerate(zip(left, right)):
            self.assertEqual(chars[0], chars[1], msg=_msg % (i, chars[0], chars[1]))

    def test_filter(self):
        self.assertEqual(Book.objects.filter(tags__contains='sex').count(), 1)
        self.assertEqual(Book.objects.filter(tags__contains='boring').count(), 0)

    def test_values_list(self):
        tag_list_list = Book.objects.all().values_list('tags', flat=True)
        categories_list_list = Book.objects.all().values_list('categories', flat=True)

        # Workaround for Django bug #9619
        # https://code.djangoproject.com/ticket/9619
        # For Django 1.6 and 1.7, calling values() or values_list() doesn't
        # call Field.from_db_field, it simply returns a Python representation
        # of the data in the database (which in our case is a string of
        # comma-separated values). The bug was fixed in Django 1.8+.
        if VERSION >= (1, 6) and VERSION < (1, 8):
            self.assertStringEqual(tag_list_list, [u('sex,work,happy')])
            self.assertStringEqual(categories_list_list, [u('1,3,5')])
        else:
            self.assertListEqual(tag_list_list, [['sex', 'work', 'happy']])
            self.assertListEqual(categories_list_list, [['1', '3', '5']])

    def test_form(self):
        form_class = modelform_factory(Book, fields=('title', 'tags', 'categories'))
        self.assertEqual(len(form_class.base_fields), 3)
        form = form_class({'title': 'new book',
                           'categories': '1,2'})
        if form.is_valid():
            form.save()

    def test_object(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.get_tags_display(), 'Sex, Work, Happy')
        self.assertEqual(book.get_tags_list(), ['Sex', 'Work', 'Happy'])
        self.assertEqual(book.get_categories_display(), 'Handbooks and manuals by discipline, Books of literary criticism, Books about literature')
        self.assertEqual(book.get_categories_list(), ['Handbooks and manuals by discipline', 'Books of literary criticism', 'Books about literature'])

        self.assertEqual(book.get_tags_list(), book.get_tags_display().split(', '))
        self.assertEqual(book.get_categories_list(), book.get_categories_display().split(', '))

    def test_validate(self):
        book = Book.objects.get(id=1)
        get_field(Book, 'tags').clean(['sex', 'work'], book)
        try:
            get_field(Book, 'tags').clean(['sex1', 'work'], book)
            raise AssertionError()
        except ValidationError:
            pass

        get_field(Book, 'categories').clean(['1', '2', '3'], book)
        try:
            get_field(Book, 'categories').clean(['1', '2', '3', '4'], book)
            raise AssertionError()
        except ValidationError:
            pass
        try:
            get_field(Book, 'categories').clean(['11', '12', '13'], book)
            raise AssertionError()
        except ValidationError:
            pass

    def test_serializer(self):
        book = Book.objects.get(id=1)
        self.assertEqual(get_field(Book, 'tags').value_to_string(book), 'sex,work,happy')
        self.assertEqual(get_field(Book, 'categories').value_to_string(book), '1,3,5')

    def test_flatchoices(self):
        self.assertEqual(get_field(Book, 'published_in').flatchoices, list(PROVINCES + STATES))

    def test_named_groups(self):
        self.assertEqual(get_field(Book, 'published_in').choices, PROVINCES_AND_STATES)

    def test_named_groups_form(self):
        form_class = modelform_factory(Book, fields=('published_in',))
        self.assertEqual(len(form_class.base_fields), 1)
        form = form_class(initial={'published_in': ['BC', 'AK']})

        expected_html = u("""<p><label for="id_published_in_0">Province or State:</label> <ul id="id_published_in"><li>Canada - Provinces<ul id="id_published_in_0"><li><label for="id_published_in_0_0"><input id="id_published_in_0_0" name="published_in" type="checkbox" value="AB" /> Alberta</label></li>\n"""
                          """<li><label for="id_published_in_0_1"><input checked="checked" id="id_published_in_0_1" name="published_in" type="checkbox" value="BC" /> British Columbia</label></li></ul></li>\n"""
                          """<li>USA - States<ul id="id_published_in_1"><li><label for="id_published_in_1_0"><input checked="checked" id="id_published_in_1_0" name="published_in" type="checkbox" value="AK" /> Alaska</label></li>\n"""
                          """<li><label for="id_published_in_1_1"><input id="id_published_in_1_1" name="published_in" type="checkbox" value="AL" /> Alabama</label></li>\n"""
                          """<li><label for="id_published_in_1_2"><input id="id_published_in_1_2" name="published_in" type="checkbox" value="AZ" /> Arizona</label></li></ul></li></ul></p>""")

        actual_html = form.as_p()

        if (1, 11) <= VERSION < (2, 0):
            # Django 1.11+ does not assign 'for' attributes on labels if they
            # are group labels
            expected_html = expected_html.replace('label for="id_published_in_0"', 'label')

        if VERSION < (1, 6):
            # Django 1.6 renders the Python repr() for each group (eg: tuples
            # with HTML entities), so we skip the test for that version
            self.assertEqual(expected_html.replace('\n', ''), actual_html.replace('\n', ''))

        if VERSION >= (1, 7):
            self.assertHTMLEqual(expected_html, actual_html)


class MultiSelectUtilsTestCase(TestCase):
    def test_get_max_length_max_length_is_not_none(self):
        self.assertEqual(get_max_length([], 5), 5)

    def test_get_max_length_max_length_is_none_and_choices_is_empty(self):
        self.assertEqual(get_max_length([], None), 200)

    def test_get_max_length_max_length_is_none_and_choices_is_not_empty(self):
        choices = [
            ('key1', 'value1'),
            ('key2', 'value2'),
            ('key3', 'value3'),
        ]
        self.assertEqual(get_max_length(choices, None), 14)

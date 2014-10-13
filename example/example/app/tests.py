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

from django.core.exceptions import ValidationError
from django.forms.models import modelform_factory
from django.test import TestCase

from example.app.models import Book


class MultiSelectTestCase(TestCase):

    fixtures = ['data.json']

    def test_filter(self):
        self.assertEqual(Book.objects.filter(tags__contains='sex').count(), 1)
        self.assertEqual(Book.objects.filter(tags__contains='boring').count(), 0)

    def test_form(self):
        form_class = modelform_factory(Book)
        self.assertEqual(len(form_class.base_fields), 3)
        form = form_class({'title': 'new book',
                           'categories': '1,2'})
        if form.is_valid():
            form.save()

    def test_object(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.get_tags_display(), 'Sex, Work, Happy')
        self.assertEqual(book.get_categories_display(), 'Handbooks and manuals by discipline, Books of literary criticism, Books about literature')

    def test_validate(self):
        book = Book.objects.get(id=1)
        Book._meta.get_field_by_name('tags')[0].clean(['sex', 'work'], book)
        try:
            Book._meta.get_field_by_name('tags')[0].clean(['sex1', 'work'], book)
            raise AssertionError()
        except ValidationError:
            pass

        Book._meta.get_field_by_name('categories')[0].clean(['1', '2', '3'], book)
        try:
            Book._meta.get_field_by_name('categories')[0].clean(['1', '2', '3', '4'], book)
            raise AssertionError()
        except ValidationError:
            pass
        try:
            Book._meta.get_field_by_name('categories')[0].clean(['11', '12', '13'], book)
            raise AssertionError()
        except ValidationError:
            pass

    def test_serializer(self):
        book = Book.objects.get(id=1)
        self.assertEqual(Book._meta.get_field_by_name('tags')[0].value_to_string(book), 'sex,work,happy')
        self.assertEqual(Book._meta.get_field_by_name('categories')[0].value_to_string(book), '1,3,5')

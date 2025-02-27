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
# along with this software.  If not, see <https://www.gnu.org/licenses/>.

from django.core.exceptions import ValidationError
from django.forms.models import modelform_factory
from django.test import TestCase

from multiselectfield.utils import get_max_length

from .models import Book, PROVINCES, STATES, PROVINCES_AND_STATES, ONE, TWO


class MultiSelectTestCase(TestCase):

    fixtures = ['app_data.json']
    maxDiff = 4000

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

        # assertCountEqual also ensures that the elements are the same (ignoring list order)
        # https://docs.python.org/3.2/library/unittest.html#unittest.TestCase.assertCountEqual
        self.assertCountEqual(tag_list_list, [['sex', 'work', 'happy']])
        self.assertCountEqual(categories_list_list, [['1', '3', '5']])

    def test_form(self):
        form_class = modelform_factory(Book, fields=('title', 'tags', 'categories'))
        self.assertEqual(len(form_class.base_fields), 3)
        form = form_class({'title': 'new book',
                           'categories': '1,2'})
        if form.is_valid():
            form.save()

    def test_empty_update(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.get_chapters_list(), ["Chapter I"])
        book.chapters = {}
        book.save(update_fields=['chapters'])
        self.assertTrue(len(book.chapters) == 0)

    def test_single_update(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.get_chapters_list(), ["Chapter I"])
        book.chapters = {ONE}
        book.save(update_fields=['chapters'])
        self.assertEqual(book.get_chapters_list(), ["Chapter I"])

    def test_multiple_update(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.get_chapters_list(), ["Chapter I"])
        book.chapters = {ONE, TWO}
        book.save(update_fields=['chapters'])
        self.assertEqual(book.get_chapters_list(), ["Chapter I", "Chapter II"])

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
        Book._meta.get_field('tags').clean(['sex', 'work'], book)
        try:
            Book._meta.get_field('tags').clean(['sex1', 'work'], book)
            raise AssertionError()
        except ValidationError:
            pass

        Book._meta.get_field('categories').clean(['1', '2', '3'], book)
        try:
            Book._meta.get_field('categories').clean(['1', '2', '3', '4'], book)
            raise AssertionError()
        except ValidationError:
            pass
        try:
            Book._meta.get_field('categories').clean(['11', '12', '13'], book)
            raise AssertionError()
        except ValidationError:
            pass

    def test_serializer(self):
        book = Book.objects.get(id=1)
        self.assertEqual(Book._meta.get_field('tags').value_to_string(book), 'sex,work,happy')
        self.assertEqual(Book._meta.get_field('categories').value_to_string(book), '1,3,5')

    def test_flatchoices(self):
        self.assertEqual(Book._meta.get_field('published_in').flatchoices, list(PROVINCES + STATES))

    def test_named_groups(self):
        # We can't use a single self.assertEqual here, because model subchoices may be lists or tuples
        # Iterate through the parent choices
        for book_choices, province_or_state_choice in zip(Book._meta.get_field('published_in').choices, PROVINCES_AND_STATES):
            parent_book_choice, *book_subchoices = book_choices
            parent_pors_choice, *pors_subchoices = province_or_state_choice
            # Check the parent keys
            self.assertEqual(parent_book_choice, parent_pors_choice)
            # Iterate through all of the subchoices
            for book_subchoice, pors_subchoice in zip(book_subchoices, pors_subchoices):
                # The model subchoices might be tuples, so make sure to convert both to lists
                self.assertEqual(list(book_subchoice), list(pors_subchoice))

    def test_named_groups_form(self):
        form_class = modelform_factory(Book, fields=('published_in',))
        self.assertEqual(len(form_class.base_fields), 1)
        form = form_class(initial={'published_in': ['BC', 'AK']})

        expected_html = """
            <p>
              <label>
                Province or State:
              </label>
              <div id="id_published_in">
                <div>
                  <label>
                    Canada - Provinces
                  </label>
                  <div>
                    <label for="id_published_in_0_0">
                      <input id="id_published_in_0_0" name="published_in" type="checkbox" value="AB" />
                      Alberta
                    </label>
                  </div>
                  <div>
                    <label for="id_published_in_0_1">
                      <input checked id="id_published_in_0_1" name="published_in" type="checkbox" value="BC" />
                      British Columbia
                    </label>
                  </div>
                </div>
                <div>
                  <label>
                    USA - States
                  </label>
                  <div>
                    <label for="id_published_in_1_0">
                      <input checked id="id_published_in_1_0" name="published_in" type="checkbox" value="AK" />
                      Alaska
                    </label>
                  </div>
                  <div>
                    <label for="id_published_in_1_1">
                      <input id="id_published_in_1_1" name="published_in" type="checkbox" value="AL" />
                      Alabama
                    </label>
                  </div>
                  <div>
                    <label for="id_published_in_1_2">
                      <input id="id_published_in_1_2" name="published_in" type="checkbox" value="AZ" />
                      Arizona
                    </label>
                  </div>
                </div>
              </div>
            </p>
            """

        actual_html = form.as_p()
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

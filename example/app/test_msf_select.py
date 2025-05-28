from django.db import models
from django.test.testcases import TestCase

from multiselectfield import MultiSelectField

from .models import Book


class MsfSelectTestCase(TestCase):
    fixtures = ['app_data.json']

    def test_valid_select(self):
        """
        Should be able to use a multiselectfield result to select
        See
        https://github.com/goinnn/django-multiselectfield/pull/135
        """
        book = Book.objects.first()
        result = Book.objects.filter(categories=book.categories).only('pk')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].pk, book.pk)
        self.assertIn(member='1,3,5', container=str(result.query))


class MSFListStrTestCase(TestCase):
    def test_msf_list_str_with_string_choices(self):
        CHOICE1 = '1'
        CHOICE2 = '2'
        CHOICE3 = '3'
        CHOICE4 = '4'
        CHOICES = ((CHOICE1, 'A'),
                   (CHOICE2, 'B'),
                   (CHOICE3, 'C'),
                   (CHOICE4, 'D'))

        class TestModel(models.Model):
            options = MultiSelectField(choices=CHOICES)

        instance = TestModel(options=[CHOICE1, CHOICE2])

        expected = "['1', '2']"
        actual = str(instance.options)

        self.assertEqual(actual, expected)

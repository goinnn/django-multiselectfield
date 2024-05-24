from django.test.testcases import TestCase

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

django-multiselectfield
=======================

.. image:: https://github.com/goinnn/django-multiselectfield/actions/workflows/tests.yaml/badge.svg
    :target: https://github.com/goinnn/django-multiselectfield/actions/workflows/tests.yaml

.. image:: https://coveralls.io/repos/goinnn/django-multiselectfield/badge.png?branch=master
    :target: https://coveralls.io/r/goinnn/django-multiselectfield

.. image:: https://badge.fury.io/py/django-multiselectfield.png
    :target: https://badge.fury.io/py/django-multiselectfield

A new model field and form field. With this you can get a multiple select from a choices. Stores to the database as a CharField of comma-separated values.

This egg is inspired by this `snippet <https://djangosnippets.org/snippets/1200/>`_.

Supported Python versions: 3.8+

Supported Django versions: 3.2+

Installation
============


Install with pip
----------------

.. code-block:: bash

    $ pip install django-multiselectfield

Configure your models.py
------------------------

.. code-block:: python

    from multiselectfield import MultiSelectField

    # ...

    MY_CHOICES = (('item_key1', 'Item title 1.1'),
                  ('item_key2', 'Item title 1.2'),
                  ('item_key3', 'Item title 1.3'),
                  ('item_key4', 'Item title 1.4'),
                  ('item_key5', 'Item title 1.5'))

    MY_CHOICES2 = (('1', 'Item title 2.1'),
                   ('2', 'Item title 2.2'),
                   ('3', 'Item title 2.3'),
                   ('4', 'Item title 2.4'),
                   ('5', 'Item title 2.5'))

    class MyModel(models.Model):

        # .....

        my_field = MultiSelectField(choices=MY_CHOICES, default=['item_key1', 'item_key5'])
        my_field2 = MultiSelectField(choices=MY_CHOICES2, min_choices=2, max_choices=3, max_length=3)


    # Do not use integer choices like this:

    MY_INTEGER_CHOICES2 = ((1, 'Item title 2.1'),
                           (2, 'Item title 2.2'),
                           (3, 'Item title 2.3'),
                           (4, 'Item title 2.4'),
                           (5, 'Item title 2.5'))

    # Because when MultiSelectField gets data from db, it can not know if the values are integers or strings.
    # In other words, MultiSelectField save the same data for MY_CHOICES2 and MY_INTEGER_CHOICES2


In your settings.py
-------------------

Only you need it, if you want the translation of django-multiselectfield

.. code-block:: python

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.admin',

        #.....................#

        'multiselectfield',
    )


Customizing templates
---------------------

It is possible to customize the HTML of this widget in your form template. To do so, you will need to loop through ``form.{field}.field.choices``. Here is an example that displays the field label underneath/after the checkbox for a ``MultiSelectField`` called ``providers``:

.. code-block:: HTML+Django

    {% for value, text in form.providers.field.choices %}
      <div class="ui slider checkbox">
        <input id="id_providers_{{ forloop.counter0 }}" name="{{ form.providers.name }}" type="checkbox" value="{{ value }}"{% if value in checked_providers %} checked="checked"{% endif %}>
        <label>{{ text }}</label>
      </div>
    {% endfor %}


Add a filter to the Django administration
------------------------------------------

You can see it in example project

.. code-block:: python

    from django.contrib import admin


    def _multiple_choice_filter(field_name, label):

        class MultiSelectFilter(admin.SimpleListFilter):
            title = label
            parameter_name = field_name

            def lookups(self, request, model_admin):
                return model_admin.model._meta.get_field(field_name).flatchoices

            def queryset(self, request, queryset):
                value = self.value()
                if value:
                    queryset = queryset.filter(Q(**{
                        f'{self.parameter_name}__exact': value,
                    }) | Q(**{
                        f'{self.parameter_name}__startswith': f'{value},',
                    }) | Q(**{
                        f'{self.parameter_name}__endswith': f',{value}'
                    }) | Q(**{
                        f'{self.parameter_name}__icontains': f',{value},'
                    }))

                return queryset
        return MultiSelectFilter

    class BookAdmin(admin.ModelAdmin):
        list_display = ('title', 'categories', 'tags', 'published_in')
        list_filter = (
            _multiple_choice_filter('categories', _('categories')),
            _multiple_choice_filter('tags', _('tags')),
            _multiple_choice_filter('favorite_tags', _('favourite tags')),
            _multiple_choice_filter('published_in', _('province or state')),
            _multiple_choice_filter('chapters', _('chapters')),
        )

Add a django multiselect field to list_display
----------------------------------------------

Option 1. Use get_FOO_display
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python


    @admin.register(Book)
    class BookAdmin(admin.ModelAdmin):
        list_display = ('title', 'get_categories_display',)

        @admin.display(description=_('categories'), ordering='categories')
        def get_categories_display(self, obj):
            return obj.get_categories_display()

Option 2. Monkey patching Django
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have a lot of django multiselect fields in list_display. You can see it in example project

This code is inspired for django code. It is possible that for other versions of Django you may need to adapt it.

.. code-block:: python

    from django.apps import AppConfig
    from django import VERSION
    from django.contrib.admin import utils
    from django.utils.hashable import make_hashable

    from multiselectfield.db.fields import MultiSelectField


    class AppAppConfig(AppConfig):
        name = 'app'
        verbose_name = 'app'

        def ready(self):
            if not hasattr(utils, '_original_display_for_field'):
                utils._original_display_for_field = utils.display_for_field
                utils.display_for_field = patched_display_for_field


    # Monkey patching for use multiselect field in list_display

    def patched_display_for_field(value, field, empty_value_display, avoid_link=False):
        if isinstance(field, MultiSelectField) and getattr(field, "flatchoices", None):
            try:
                flatchoices = dict(field.flatchoices)
                return ', '.join([flatchoices.get(v, empty_value_display) for v in value]) or empty_value_display
            except TypeError:
                # Allow list-like choices.
                flatchoices = dict(make_hashable(field.flatchoices))
                value = make_hashable(value)
                return ', '.join([flatchoices.get(v, empty_value_display) for v in value]) or empty_value_display

        if VERSION < (5, 2):
            return utils._original_display_for_field(value, field, empty_value_display)
        return utils._original_display_for_field(value, field, empty_value_display, avoid_link=avoid_link)


Django REST Framework
---------------------

Django REST Framework comes with a ``MultipleChoiceField`` that works perfectly with this:

.. code-block:: python

    from rest_framework import fields, serializers

    from myapp.models import MY_CHOICES, MY_CHOICES2

    class MyModelSerializer(serializers.HyperlinkedModelSerializer):
        # ...
        my_field = fields.MultipleChoiceField(choices=MY_CHOICES)
        my_field2 = fields.MultipleChoiceField(choices=MY_CHOICES2)
        # ...


Tests
=====

All tests pass on Django 3.2.0, 4.0.0, 4.1.0, 4.2.0, 5.0.0 and 5.1.0


Development
===========

You can get the last bleeding edge version of django-multiselectfield by doing a clone
of its git repository:

.. code-block:: bash

    git clone https://github.com/goinnn/django-multiselectfield


Example project
===============

There is a fully configured example project in the `example directory <https://github.com/goinnn/django-multiselectfield/tree/master/example/>`_. You can run it as usual:

.. code-block:: bash

    python manage.py migrate
    python manage.py loaddata app_data
    python manage.py runserver

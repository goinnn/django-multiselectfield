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

    MY_CHOICES2 = ((1, 'Item title 2.1'),
                   (2, 'Item title 2.2'),
                   (3, 'Item title 2.3'),
                   (4, 'Item title 2.4'),
                   (5, 'Item title 2.5'))

    class MyModel(models.Model):

        # .....

        my_field = MultiSelectField(choices=MY_CHOICES)
        my_field2 = MultiSelectField(choices=MY_CHOICES2,
                                     max_choices=3,
                                     max_length=3)


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

    python manage.py migrate  # or python manage.py syncdb --noinput
    python manage.py loaddata app_data
    python manage.py runserver

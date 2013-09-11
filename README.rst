django-multiselectfield
=======================

.. image:: https://badge.fury.io/py/django-multiselectfield.png
    :target: https://badge.fury.io/py/django-multiselectfield

.. image:: https://pypip.in/d/django-multiselectfield/badge.png
    :target: https://pypi.python.org/pypi/django-multiselectfield

A new model and form field. With this you can get a multiple select from a choices

This egg is done from a `snippet <http://djangosnippets.org/snippets/1200/>`_

Installation
============

In your settings.py
-------------------

::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.admin',

        #.....................#

        'multiselectfield',
    )


In your models.py
-----------------

::

    from multiselectfield import MultiSelectField

    ...

    MY_CHOICES = (('item_key1', 'Item title1'),
                  ('item_key2', 'Item title2'),
                  ('item_key3', 'Item title3'),
                  ('item_key4', 'Item title4'),
                  ('item_key5', 'Item title5'))

    class MyModel(models.Model):

        .....

        my_field = MultiSelectField(choices=MY_CHOICES, max_length=20)


Development
===========

You can get the last bleeding edge version of django-configfield by doing a clone
of its git repository::

  git clone https://github.com/goinnn/django-multiselectfield

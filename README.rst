django-multiselectfield
=======================

.. image:: https://travis-ci.org/goinnn/django-multiselectfield.png?branch=master
    :target: https://travis-ci.org/goinnn/django-multiselectfield

.. image:: https://coveralls.io/repos/goinnn/django-multiselectfield/badge.png?branch=master
    :target: https://coveralls.io/r/goinnn/django-multiselectfield

.. image:: https://badge.fury.io/py/django-multiselectfield.png
    :target: https://badge.fury.io/py/django-multiselectfield

A new model field and form field. With this you can get a multiple select from a choices. Stores to the database as a CharField of comma-separated values.

This egg is inspired by this `snippet <http://djangosnippets.org/snippets/1200/>`_.

Supported Python versions: 2.6, 2.7, 3.3+

Supported Django versions: 1.4-1.10+

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


Known Bugs and Limitations
==========================

All tests pass on Django 1.4, 1.5, and 1.8+, so if you can, use a modern version of Django. However, if you must use Django 1.6 or 1.7 there are two known issues you will need to be aware of:

1. `Named groups <https://github.com/goinnn/django-multiselectfield/pull/30#issue-52149983>`_ do not render properly in Django 1.6. The workaround is to manually render the field in your form or use a custom widget. If your workaround is suitably generic, please submit a pull request with it.

2. Only in Django 1.6 and 1.7, due to `Django bug #9619 <https://code.djangoproject.com/ticket/9619>`_, passing a MultiSelectField to ``values()`` or ``values_list()`` will return the database representation of the field (a string of comma-separated values). The workaround is to manually call ``.split(',')`` on the result.

   The Django bug was introduced in Django 1.6 and is fixed in Django 1.8 and onward, so ``values()`` and ``values_list()`` return a vanilla Python list of values for Django <= 1.5 and Django >= 1.8.

   See `issue #40 <https://github.com/goinnn/django-multiselectfield/issues/40>`_ for discussion about this bug.


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

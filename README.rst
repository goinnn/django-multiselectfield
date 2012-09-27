django-multiselectfield
=======================

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

    class MyModel(models.Model):

        .....

        my_field = MultiSelectField(verbose_name=_('xxx'), choices=MY_CHOICES)


Development
===========

You can get the last bleeding edge version of django-configfield by doing a clone
of its hg repository::

  git clone https://github.com/goinnn/django-multiselectfield

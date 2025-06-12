=======================
django-multiselectfield
=======================

.. image:: https://github.com/goinnn/django-multiselectfield/actions/workflows/tests.yaml/badge.svg
    :target: https://github.com/goinnn/django-multiselectfield/actions/workflows/tests.yaml

.. image:: https://coveralls.io/repos/goinnn/django-multiselectfield/badge.png?branch=master
    :target: https://coveralls.io/r/goinnn/django-multiselectfield

.. image:: https://badge.fury.io/py/django-multiselectfield.png
    :target: https://badge.fury.io/py/django-multiselectfield


-------------------


Support this package by donating here! ➡️
=========================================

If you find this package useful, consider supporting it:

.. image:: https://cdn.buymeacoffee.com/buttons/v2/arial-yellow.png
    :target: https://www.buymeacoffee.com/goinnn
    :alt: Buy Me a Coffee
    :height: 40px

.. image:: https://img.shields.io/badge/PayPal-badge?style=plastic&logo=paypal&color=white
    :target: https://www.paypal.com/paypalme/goinnn
    :alt: Paypal
    :height: 40px


-------------------

django-multiselectfield provides new model and form fields for Django models, allowing multiple selections from a list of choices. The selected values are stored in the database as a CharField containing a comma-separated values.

This package is inspired by this `snippet <https://djangosnippets.org/snippets/1200/>`_.

*Note: This snippet is from 2008, and a lot has changed since then.*

**Supported Python versions**: 3.8+

**Supported Django versions**: 3.2+

1. Installation
================


1.1 Install with pip
---------------------

.. code-block:: bash

    $ pip install django-multiselectfield

1.2 Configure your models.py
----------------------------

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

    # Because when MultiSelectField retrieves data from db, it cannot know if the values are integers or strings.
    # In other words, MultiSelectField save the same data for MY_CHOICES2 and MY_INTEGER_CHOICES2
    # Or in practice it should be the same MY_CHOICES2 and MY_INTEGER_CHOICES2


1.3 In your settings.py
-----------------------

Only required if you want the translation of django-multiselectfield or need its static files.

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

1.4 SortMultiSelectField
------------------------

Since version 1.0.0 (2025-06-12), this package also includes a another field type called: SortMultiSelectField.

For this field to work, you need to include `jQuery <https://jquery.com/download/>`_ (already included in the Django admin) and `jQuery UI <https://jqueryui.com/download/>`_.

You can include them by updating the ModelAdmin’s form or directly in change_form.html (less efficient but faster), as shown in the `example project: change_form.html line 11 <https://github.com/goinnn/django-multiselectfield/blob/b7d113a4a1ad6b35698126729264942e30e30039/example/templates/admin/change_form.html#L11>`_.

1.5 Other recommendations
-------------------------

`As django recommended: <https://docs.djangoproject.com/en/5.2/ref/models/fields/#django.db.models.Field.null>`_ Avoid using null on string-based fields such as CharField and TextField.

MultiSelectField is based on CharField (MultiSelectField inheritances of CharField). So, if the field is not required, use only blank=True (null=False by default):

.. code-block:: python

    class MyModel(models.Model):

        # .....

        my_field = MultiSelectField(choices=MY_CHOICES, blank=True)


2. Custom and integrations
===========================

2.1 Customizing templates
--------------------------

You can customize the HTML of this widget in your form template. To do so, you will need to loop through ``form.{field}.field.choices``. Here is an example that displays the field label underneath/after the checkbox for a ``MultiSelectField`` called ``providers``:

.. code-block:: HTML+Django

    {% for value, text in form.providers.field.choices %}
      <div class="ui slider checkbox">
        <input id="id_providers_{{ forloop.counter0 }}" name="{{ form.providers.name }}" type="checkbox" value="{{ value }}"{% if value in checked_providers %} checked="checked"{% endif %}>
        <label>{{ text }}</label>
      </div>
    {% endfor %}


2.2 Fixing CSS alignment in the Django administration
------------------------------------------------------

This fixes alignment. The labels appear slightly lower than the checkboxes, and the label width is very small.

Include the following CSS file: multiselectfield/css/admin-multiselectfield.css

You can include it by updating the ModelAdmin’s form or directly in change_form.html (less efficient but faster), as shown in the `example project: change_form.html line 7 <https://github.com/goinnn/django-multiselectfield/blob/b7d113a4a1ad6b35698126729264942e30e30039/example/templates/admin/change_form.html#L7>`_.

2.3 Add a filter to the Django administration
----------------------------------------------

You can see it in `example project: admin.py line 23 <https://github.com/goinnn/django-multiselectfield/blob/4ee111e11e2f3a51aa693c0863ee64d93b4a097d/example/app/admin.py#L23>`_

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

2.4 Add a django multiselect field to list_display in Django administration
----------------------------------------------------------------------------

Django doesn't provide built-in support for custom fields.


2.4.1 Option 1. Use get_FOO_display
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Change them individually

.. code-block:: python


    @admin.register(Book)
    class BookAdmin(admin.ModelAdmin):
        list_display = ('title', 'get_categories_display',)

        @admin.display(description=_('categories'), ordering='categories')
        def get_categories_display(self, obj):
            return obj.get_categories_display()

2.4.2 Option 2. Monkey patching Django
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have many django multiselect fields in list_display, the previous option can be much work.

You can see it in the `example project: apps.py line 34 <https://github.com/goinnn/django-multiselectfield/blob/65376239ae7491414f896adb4d314349ff7c2667/example/app/apps.py#L34>`_.

This code is inspired by django code. It is possible that for other versions of Django you may need to adapt it.

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
                return ', '.join([str(flatchoices.get(v, empty_value_display)) for v in value]) or empty_value_display
            except TypeError:
                # Allow list-like choices.
                flatchoices = dict(make_hashable(field.flatchoices))
                value = make_hashable(value)
                return ', '.join([str(flatchoices.get(v, empty_value_display)) for v in value]) or empty_value_display

        if VERSION < (5, 2):
            return utils._original_display_for_field(value, field, empty_value_display)
        return utils._original_display_for_field(value, field, empty_value_display, avoid_link=avoid_link)

2.5 Add support for read-only fields in the Django administration
-----------------------------------------------------------------

Django doesn't provide built-in support for custom fields.

You can see it in the `example project: apps.py line 52 <https://github.com/goinnn/django-multiselectfield/blob/65376239ae7491414f896adb4d314349ff7c2667/example/app/apps.py#L52>`_. Log in to the Django admin in the sample project using the following credentials: user-readonly / DMF-123.

This code is inspired by django code. It is possible that for other versions of Django you may need to adapt it.

.. code-block:: python

    from django.apps import AppConfig
    from django.contrib.admin.helpers import AdminReadonlyField
    from django.contrib.admin.utils import display_for_field, lookup_field
    from django.core.exceptions import ObjectDoesNotExist
    from django.db.models.fields.related import (
        ForeignObjectRel,
        ManyToManyRel,
        OneToOneField,
    )
    from django.template.defaultfilters import linebreaksbr
    from django.utils.html import conditional_escape
    from django.utils.translation import gettext_lazy as _

    from multiselectfield.db.fields import MultiSelectField


    class AppAppConfig(AppConfig):
        name = 'app'
        verbose_name = 'app'

        def ready(self):
            if not hasattr(AdminReadonlyField, '_original_contents'):
                AdminReadonlyField._original_contents = AdminReadonlyField.contents
                AdminReadonlyField.contents = patched_contents

    def patched_contents(self):
        from django.contrib.admin.templatetags.admin_list import _boolean_icon

        field, obj, model_admin = (
            self.field["field"],
            self.form.instance,
            self.model_admin,
        )
        try:
            f, attr, value = lookup_field(field, obj, model_admin)
        except (AttributeError, ValueError, ObjectDoesNotExist):
            result_repr = self.empty_value_display
        else:
            if field in self.form.fields:
                widget = self.form[field].field.widget
                # This isn't elegant but suffices for contrib.auth's
                # ReadOnlyPasswordHashWidget.
                if getattr(widget, "read_only", False):
                    return widget.render(field, value)
            if f is None:
                if getattr(attr, "boolean", False):
                    result_repr = _boolean_icon(value)
                else:
                    if hasattr(value, "__html__"):
                        result_repr = value
                    else:
                        result_repr = linebreaksbr(value)
            else:
                if isinstance(f.remote_field, ManyToManyRel) and value is not None:
                    result_repr = ", ".join(map(str, value.all()))
                elif (
                    isinstance(f.remote_field, (ForeignObjectRel, OneToOneField))
                    and value is not None
                ):
                    result_repr = self.get_admin_url(f.remote_field, value)
                # Custom: start
                elif isinstance(f, MultiSelectField):
                    if value in f.empty_values:
                        result_repr = self.empty_value_display
                    else:
                        result_repr = getattr(obj, f'get_{f.name}_display')()
                # Custom: end
                else:
                    result_repr = display_for_field(value, f, self.empty_value_display)
                result_repr = linebreaksbr(result_repr)
        return conditional_escape(result_repr)


2.6 Django REST Framework
-------------------------

Django REST Framework comes with a ``MultipleChoiceField`` that works perfectly with this:

.. code-block:: python

    from rest_framework import fields, serializers

    from myapp.models import MY_CHOICES, MY_CHOICES2

    class MyModelSerializer(serializers.HyperlinkedModelSerializer):
        # ...
        my_field = fields.MultipleChoiceField(choices=MY_CHOICES)
        my_field2 = fields.MultipleChoiceField(choices=MY_CHOICES2)
        # ...

3. Tests
========

All tests pass on Django 3.2.0, 4.0.0, 4.1.0, 4.2.0, 5.0.0 and 5.1.0


4. Development
==============

You can get the last bleeding edge version of django-multiselectfield by doing a clone of its git repository:

.. code-block:: bash

    git clone https://github.com/goinnn/django-multiselectfield


5. Example project
===================

There is a fully configured example project in the `example directory <https://github.com/goinnn/django-multiselectfield/tree/master/example/>`_. You can run it as usual:

.. code-block:: bash

    python manage.py migrate
    python manage.py loaddata app_data
    python manage.py runserver
    # And go to http://localhost:8000. You will be automatically authenticated as a superuser.

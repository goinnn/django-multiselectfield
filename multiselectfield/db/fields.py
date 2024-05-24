# -*- coding: utf-8 -*-
# Copyright (c) 2012 by Pablo Martín <goinnn@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this programe.  If not, see <http://www.gnu.org/licenses/>.

from django import VERSION
from django.db import models
from django.utils.text import capfirst
from django.core import exceptions

from ..forms.fields import MultiSelectFormField, MinChoicesValidator, MaxChoicesValidator
from ..utils import MSFList, get_max_length
from ..validators import MaxValueMultiFieldValidator


def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        for slots_var in orig_vars.get('__slots__', ()):
            orig_vars.pop(slots_var)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


class MultiSelectField(models.CharField):
    """ Choice values can not contain commas. """

    def __init__(self, *args, **kwargs):
        self.min_choices = kwargs.pop('min_choices', None)
        self.max_choices = kwargs.pop('max_choices', None)
        super(MultiSelectField, self).__init__(*args, **kwargs)
        self.max_length = get_max_length(self.choices, self.max_length)
        self.validators.append(MaxValueMultiFieldValidator(self.max_length))
        if self.min_choices is not None:
            self.validators.append(MinChoicesValidator(self.min_choices))
        if self.max_choices is not None:
            self.validators.append(MaxChoicesValidator(self.max_choices))

    def _get_flatchoices(self):
        if VERSION >= (5,):
            flat_choices = super(MultiSelectField, self).flatchoices
        else:
            flat_choices = super(MultiSelectField, self)._get_flatchoices()

        class MSFFlatchoices(list):
            # Used to trick django.contrib.admin.utils.display_for_field into
            # not treating the list of values as a dictionary key (which errors
            # out)
            def __bool__(self):
                return False
            __nonzero__ = __bool__
        return MSFFlatchoices(flat_choices)
    flatchoices = property(_get_flatchoices)

    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def get_choices_selected(self, arr_choices):
        named_groups = arr_choices and isinstance(arr_choices[0][1], (list, tuple))
        choices_selected = []
        if named_groups:
            for choice_group_selected in arr_choices:
                for choice_selected in choice_group_selected[1]:
                    choices_selected.append(str(choice_selected[0]))
        else:
            for choice_selected in arr_choices:
                choices_selected.append(str(choice_selected[0]))
        return choices_selected

    def value_to_string(self, obj):
        try:
            value = self._get_val_from_obj(obj)
        except AttributeError:
            value = super(MultiSelectField, self).value_from_object(obj)
        return self.get_prep_value(value)

    def validate(self, value, model_instance):
        arr_choices = self.get_choices_selected(self.get_choices_default())
        for opt_select in value:
            if (opt_select not in arr_choices):
                raise exceptions.ValidationError(self.error_messages['invalid_choice'] % {"value": value})

    def get_default(self):
        default = super(MultiSelectField, self).get_default()
        if isinstance(default, int):
            default = str(default)
        return default

    def formfield(self, **kwargs):
        defaults = {'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text,
                    'choices': self.choices,
                    'flat_choices': self.flatchoices,
                    'max_length': self.max_length,
                    'min_choices': self.min_choices,
                    'max_choices': self.max_choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_prep_value(self, value):
        return '' if value is None else ",".join(map(str, value))

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared and not isinstance(value, str):
            value = self.get_prep_value(value)
        return value

    def to_python(self, value):
        choices = dict(self.flatchoices)

        if value:
            if isinstance(value, list):
                return value
            elif isinstance(value, str):
                value_list = map(lambda x: x.strip(), value.replace('，', ',').split(','))
                return MSFList(choices, value_list)
            elif isinstance(value, (set, dict)):
                return MSFList(choices, list(value))
        return MSFList(choices, [])

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.to_python(value)

    def contribute_to_class(self, cls, name):
        super(MultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            def get_list(obj):
                fieldname = name
                choicedict = dict(self.choices)
                display = []
                if getattr(obj, fieldname):
                    for value in getattr(obj, fieldname):
                        item_display = choicedict.get(value, None)
                        if item_display is None:
                            try:
                                item_display = choicedict.get(int(value), value)
                            except (ValueError, TypeError):
                                item_display = value
                        display.append(str(item_display))
                return display

            def get_display(obj):
                return ", ".join(get_list(obj))
            get_display.short_description = self.verbose_name

            setattr(cls, 'get_%s_list' % self.name, get_list)
            setattr(cls, 'get_%s_display' % self.name, get_display)

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

import sys

from django import VERSION
from django.core import exceptions, checks
from django.db import models
import six
from django.utils.text import capfirst

from ..forms.fields import MultiSelectFormField, MinChoicesValidator, MaxChoicesValidator, MultiSelectWithOtherFormField
from ..utils import get_max_length, add_other_field_in_choices
from ..validators import MaxValueMultiFieldValidator

if sys.version_info < (3,):
    string_type = unicode  # noqa: F821
else:
    string_type = str


# Code from six egg https://bitbucket.org/gutworth/six/src/a3641cb211cc360848f1e2dd92e9ae6cd1de55dd/six.py?at=default


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


class MSFList(list):

    def __init__(self, choices, *args, **kwargs):
        self.choices = choices
        super(MSFList, self).__init__(*args, **kwargs)

    def __str__(msgl):
        msg_list = [msgl.choices.get(int(i)) if i.isdigit() else msgl.choices.get(i) for i in msgl]
        return u', '.join([string_type(s) for s in msg_list])

    if sys.version_info < (3,):
        def __unicode__(self, msgl):
            return self.__str__(msgl)


class MultiSelectField(models.CharField):
    """ Choice values can not contain commas. """

    def __init__(self, *args, **kwargs):
        self.min_choices = kwargs.pop('min_choices', None)
        self.max_choices = kwargs.pop('max_choices', None)
        super(MultiSelectField, self).__init__(*args, **kwargs)
        self.max_length = get_max_length(self.choices, self.max_length)
        self.validators[0] = MaxValueMultiFieldValidator(self.max_length)
        if self.min_choices is not None:
            self.validators.append(MinChoicesValidator(self.min_choices))
        if self.max_choices is not None:
            self.validators.append(MaxChoicesValidator(self.max_choices))

    def _get_flatchoices(self):
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
                    choices_selected.append(string_type(choice_selected[0]))
        else:
            for choice_selected in arr_choices:
                choices_selected.append(string_type(choice_selected[0]))
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
                if VERSION >= (1, 6):
                    raise exceptions.ValidationError(self.error_messages['invalid_choice'] % {"value": value})
                else:
                    raise exceptions.ValidationError(self.error_messages['invalid_choice'] % value)

    def get_default(self):
        default = super(MultiSelectField, self).get_default()
        if isinstance(default, int):
            default = string_type(default)
        return default

    def formfield(self, **kwargs):
        defaults = {'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text,
                    'choices': self.choices,
                    'max_length': self.max_length,
                    'max_choices': self.max_choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_prep_value(self, value):
        return '' if value is None else ",".join(map(str, value))

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared and not isinstance(value, string_type):
            value = self.get_prep_value(value)
        return value

    def to_python(self, value):
        choices = dict(self.flatchoices)

        if value:
            if isinstance(value, list):
                return value
            elif isinstance(value, string_type):
                value_list = map(lambda x: x.strip(), value.replace(u'，', ',').split(','))
                return MSFList(choices, value_list)
            elif isinstance(value, (set, dict)):
                return MSFList(choices, list(value))
        return MSFList(choices, [])

    if VERSION < (2,):
        def from_db_value(self, value, expression, connection, context):
            if value is None:
                return value
            return self.to_python(value)
    else:
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
                        display.append(string_type(item_display))
                return display

            def get_display(obj):
                return ", ".join(get_list(obj))

            get_display.short_description = self.verbose_name

            setattr(cls, 'get_%s_list' % self.name, get_list)
            setattr(cls, 'get_%s_display' % self.name, get_display)


if VERSION < (1, 8):
    MultiSelectField = add_metaclass(models.SubfieldBase)(MultiSelectField)

try:
    from south.modelsinspector import add_introspection_rules

    add_introspection_rules([], ['^multiselectfield\.db.fields\.MultiSelectField'])
except ImportError:
    pass


class OtherMultiSelectFieldList(MSFList):
    def __str__(self):
        selected_choice_list = [self.choices.get(int(i)) if i.isdigit() else (self.choices.get(i) or i) for i in self]
        return u', '.join([string_type(s) for s in selected_choice_list])

class MultiSelectWithOtherField(MultiSelectField):
    """
        This class is a Django Model field class that supports
        multi select along with other option
        The `other_max_length` parameter is required for this
        Choice keys can not contain commas and other field can not contain
        pipe character i.e. `|`
    """

    def __init__(self, other_max_length=None, *args, **kwargs):
        self.other_max_length = other_max_length
        self.other_delimiter = kwargs.get('other_delimiter', '|')
        if kwargs.get('max_length') is None and other_max_length is not None:
            choice_max_length = get_max_length(kwargs['choices'], kwargs.get('max_length'))
            kwargs['max_length'] = choice_max_length + other_max_length

        if kwargs.get('choices'):
            kwargs['choices'] = add_other_field_in_choices(kwargs['choices'])

        super(MultiSelectWithOtherField, self).__init__(*args, **kwargs)

        self.error_messages.update({
            'invalid_char': 'value %s contains invalid character `{other_delimiter}`'.format(
                other_delimiter=self.other_delimiter)
        })

    def get_prep_value(self, value):
        selected_value = other_value = ''
        choice_values = [choice[0] for choice in self.choices]
        if value:
            for val in value:
                if val in choice_values:
                    selected_value += val + ','
                else:
                    other_value = val

            selected_value += self.other_delimiter + other_value
        return selected_value

    def formfield(self, **kwargs):
        defaults = {
            'required': not self.blank,
            'label': capfirst(self.verbose_name),
            'help_text': self.help_text,
            'choices': self.choices,
            'max_length': self.max_length,
            'max_choices': self.max_choices,
            'other_max_length': self.other_max_length
        }
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectWithOtherFormField(**defaults)

    def validate(self, value, model_instance):
        """
        This function is to validate the input values for multi select field,
        however we are implementing field with support of other input filed
        we are disabling validations to let other input text(other option)
        pass to the database.

        :param value: list of all selected choice with other text.
        :param model_instance: current model instance for with it is saving data.
        :return: None
        """
        for opt_select in value:
            if self.other_delimiter in opt_select:
                raise exceptions.ValidationError(self.error_messages['invalid_char'] % value)

    def to_python(self, value):
        choices = dict(self.flatchoices)
        if value:
            if isinstance(value, list):
                return value
            elif isinstance(value, string_type):
                choices_str = value.replace(self.other_delimiter, '')
                selected_choices = [choice for choice in choices_str.split(',') if choice.strip()]
                return OtherMultiSelectFieldList(choices, selected_choices)
            elif isinstance(value, (set, dict)):
                return MSFList(choices, list(value))
        return MSFList(choices, [])

    def _check_other_max_length_attribute(self, **kwargs):
        if self.other_max_length is None:
            return [
                checks.Error(
                    "MultiSelectWithOtherField must define a 'other_max_length' attribute.",
                    obj=self,
                    id='fields.E120',
                )
            ]
        elif not isinstance(self.other_max_length, six.integer_types) or self.other_max_length <= 0:
            return [
                checks.Error(
                    "'other_max_length' must be a positive integer.",
                    obj=self,
                    id='fields.E121',
                )
            ]
        else:
            return []

    def check(self, **kwargs):
        errors = super(MultiSelectWithOtherField, self).check(**kwargs)
        errors.extend(self._check_other_max_length_attribute(**kwargs))
        return errors

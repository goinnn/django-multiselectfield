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
# along with this programe.  If not, see <https://www.gnu.org/licenses/>.

from django import VERSION
from django.db import models
from django.utils.text import capfirst
from django.core import exceptions

from ..forms.fields import SortMultiSelectFormField

from ..forms.fields import MultiSelectFormField, MinChoicesValidator, MaxChoicesValidator
from ..utils import get_max_length
from ..validators import MaxValueMultiFieldValidator


class MultiSelectField(models.CharField):
    """ Choice values can not contain commas. """

    def __init__(self, *args, **kwargs):
        self.min_choices = kwargs.pop('min_choices', None)
        self.max_choices = kwargs.pop('max_choices', None)
        super().__init__(*args, **kwargs)
        self.max_length = get_max_length(self.choices, self.max_length)
        if VERSION <= (4, 1):
            self.validators[0] = MaxValueMultiFieldValidator(self.max_length)
        else:
            self.validators.append(MaxValueMultiFieldValidator(self.max_length))
        if self.min_choices is not None:
            self.validators.append(MinChoicesValidator(self.min_choices))
        if self.max_choices is not None:
            self.validators.append(MaxChoicesValidator(self.max_choices))

    def value_to_string(self, obj):
        value = super().value_from_object(obj)
        return self.get_prep_value(value)

    def validate(self, value, model_instance):
        if not self.editable:
            # Skip validation for non-editable fields.
            return
        if self.choices is not None and value not in self.empty_values:
            arr_choices = dict(self.flatchoices).keys()
            for opt_select in value:
                if opt_select not in arr_choices:
                    raise exceptions.ValidationError(self.error_messages['invalid_choice'] % {"value": value})

        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages["null"], code="null")

        if not self.blank and value in self.empty_values:
            raise exceptions.ValidationError(self.error_messages["blank"], code="blank")

    def formfield(self, **kwargs):
        if isinstance(kwargs.get('form_class'), MultiSelectFormField):
            return kwargs.get('form_class')

        defaults = {
            'required': not self.blank,
            'label': capfirst(self.verbose_name),
            'help_text': self.help_text,
            'choices': self.choices,
            'max_length': self.max_length,
            'min_choices': self.min_choices,
            'max_choices': self.max_choices
        }
        if self.has_default():
            defaults['initial'] = self.get_default()

        defaults.update(kwargs)
        form_class = defaults.pop('form_class', MultiSelectFormField) or MultiSelectFormField

        return form_class(**defaults)

    def get_prep_value(self, value):
        if isinstance(value, str):
            return value
        if value is None:
            return ''
        # It is a list
        return ",".join(value)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if not value:
            return []
        # It is a string
        return value.split(',')

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.to_python(value)

    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        if self.choices:
            def get_list(obj):
                fieldname = name
                choicedict = dict(self.flatchoices)
                display = []
                if getattr(obj, fieldname):
                    for value in getattr(obj, fieldname):
                        item_display = choicedict.get(value, value)
                        display.append(str(item_display))
                return display

            def get_display(obj):
                return ", ".join(get_list(obj))
            get_display.short_description = self.verbose_name

            setattr(cls, 'get_%s_list' % self.name, get_list)
            setattr(cls, 'get_%s_display' % self.name, get_display)


class SortMultiSelectField(MultiSelectField):

    def formfield(self, **kwargs):
        if isinstance(kwargs.get('form_class'), SortMultiSelectFormField):
            return kwargs.get('form_class')

        defaults = {
            'required': not self.blank,
            'label': capfirst(self.verbose_name),
            'help_text': self.help_text,
            'choices': self.choices,
            'max_length': self.max_length,
            'min_choices': self.min_choices,
            'max_choices': self.max_choices
        }
        if self.has_default():
            defaults['initial'] = self.get_default()

        defaults.update(kwargs)
        form_class = defaults.pop('form_class', SortMultiSelectFormField) or SortMultiSelectFormField

        return form_class(**defaults)

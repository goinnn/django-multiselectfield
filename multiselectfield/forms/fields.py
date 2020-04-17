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

from django import forms
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple
from django.utils.translation import ugettext_lazy as _

from ..utils import get_max_length
from ..validators import MaxValueMultiFieldValidator, MinChoicesValidator, MaxChoicesValidator


class MultiSelectFormField(forms.MultipleChoiceField):
    widget = forms.CheckboxSelectMultiple

    def __init__(self, *args, **kwargs):
        self.min_choices = kwargs.pop('min_choices', None)
        self.max_choices = kwargs.pop('max_choices', None)
        self.max_length = kwargs.pop('max_length', None)
        super(MultiSelectFormField, self).__init__(*args, **kwargs)
        self.max_length = get_max_length(self.choices, self.max_length)
        self.validators.append(MaxValueMultiFieldValidator(self.max_length))
        if self.max_choices is not None:
            self.validators.append(MaxChoicesValidator(self.max_choices))
        if self.min_choices is not None:
            self.validators.append(MinChoicesValidator(self.min_choices))


def get_other_values(choices, value):
    """
    This function to separate other's value from list of choices
    :param choices: list of valid choices
    :param value: list of selected choices including other's value
    :return: list of other values.
    """
    choice_values = [choice[0] for choice in choices]
    other_values = [val for val in value if val not in choice_values]
    return other_values


class CheckboxSelectMultipleWithOther(CheckboxSelectMultiple):
    """
        Widget class to handle other value filed.
    """
    other_choice = None

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(CheckboxSelectMultipleWithOther, self).create_option(name, value, label, selected, index,
                                                                            subindex, attrs)
        option.update({
            'value': self.other_choice if value == 'other' else value,
            'type': 'text' if value == 'other' else self.input_type,
            'is_other': label == 'Other'
        })
        return option

    def optgroups(self, name, value, attrs=None):
        """Return a list of optgroups for this widget."""

        other_values = get_other_values(self.choices, value)

        OTHER_CHOICE_INDEX = 0
        other_values = '' if not other_values else other_values.pop(OTHER_CHOICE_INDEX)

        self.other_choice = other_values

        return super(CheckboxSelectMultipleWithOther, self).optgroups(name, value, attrs)


class MultiSelectWithOtherFormField(MultiSelectFormField):
    """
    Form field class to handle other text input field with in the multiselect field
    """
    widget = CheckboxSelectMultipleWithOther

    def __init__(self, other_max_length=None, *args, **kwargs):
        super(MultiSelectWithOtherFormField, self).__init__(*args, **kwargs)
        self.other_max_length = other_max_length
        self.error_messages.update(
            dict(invalid_length=_('Other field value. %(value)s maximum allowed length violation.')))

    def valid_value(self, value):
        return len(value) < self.other_max_length

    def validate(self, value):
        """Validate that the input is a list or tuple."""
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')

        if self.other_max_length is not None:

            other_values = get_other_values(self.choices, value)
            for val in other_values:
                if not self.valid_value(val):
                    raise ValidationError(
                        self.error_messages['invalid_length'],
                        code='invalid_length',
                        params={'value': val},
                    )

    def clean(self, value):
        value = [val for val in value if val not in self.empty_values]
        return super(MultiSelectWithOtherFormField, self).clean(value)

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
from django import forms
from django.forms.widgets import ChoiceWidget, CheckboxSelectMultiple
from django.utils.encoding import force_text

from ..utils import get_max_length
from ..validators import MaxValueMultiFieldValidator, MinChoicesValidator, MaxChoicesValidator


class CheckboxSelectMultipleSorted(CheckboxSelectMultiple):
    allow_multiple_selected = True
    input_type = 'checkbox'
    template_name = 'multiselectfield/multi_sorted.html'
    option_template_name = 'django/forms/widgets/checkbox_option.html'

    class Media:
        js = (
            'multiselectfield/widget.js',
            'multiselectfield/jquery-ui.js',
        )
        css = {'screen': (
            'multiselectfield/widget.css',
        )}

    @staticmethod
    def get_sort_key(arr, val):
        try:
            return arr.index(str(val))
        except ValueError:
            # Keys not selected should be present at bottom
            return sys.maxsize

    def optgroups(self, name, value, attrs=None):
        groups = super(CheckboxSelectMultipleSorted, self).optgroups(name, value, attrs=attrs)

        # No grouping
        if groups[0][0] is None:
            # Sort the options placing the selected options on top.
            groups.sort(key = lambda x: CheckboxSelectMultipleSorted.get_sort_key(value, x[1][0]['value']))
        else:
            for optGroup in groups:
                # Sort the options placing the selected options on top.
                optGroup[1].sort(key = lambda x: CheckboxSelectMultipleSorted.get_sort_key(value, x['value']))

        return groups

class MultiSelectFormField(forms.MultipleChoiceField):
    widget = CheckboxSelectMultipleSorted

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

    def has_changed(self, initial, data):
        """Implementation same as MultipleChoiceField.hasChanged() except this
        checks the order of lists as well"""
        if self.disabled:
            return False
        if initial is None:
            initial = []
        if data is None:
            data = []
        if len(initial) != len(data):
            return True

        initial_list = [force_text(value) for value in initial]
        data_list = [force_text(value) for value in data]

        return initial_list != data_list


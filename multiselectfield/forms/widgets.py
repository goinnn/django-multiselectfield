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
# along with this programe.  If not, see <https://www.gnu.org/licenses/>.
import sys

from django import forms


class SortedCheckboxSelectMultiple(forms.CheckboxSelectMultiple):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs['class'] = 'ui-pre-sortable'

    class Media:
        js = (
            'sortmultiselectfield/sortmultiselectfield.js'
        )
        css = {
            'all': ('sortmultiselectfield/sortmultiselectfield.css',)
        }

    def optgroups(self, name, value, attrs=None):
        """Return a list of optgroups for this widget."""
        groups = []
        has_selected = False
        choices = self.choices

        def index_of(val, in_list):
            try:
                return in_list.index(val)
            except ValueError:
                return sys.maxsize

        choices = sorted(choices, key=lambda choice: index_of(choice[0], value))

        for index, (option_value, option_label) in enumerate(choices):
            if option_value is None:
                option_value = ''
            subgroup = []
            if isinstance(option_label, (list, tuple)):
                group_name = option_value
                subindex = 0
                choices = option_label
            else:
                group_name = None
                subindex = None
                choices = [(option_value, option_label)]
            groups.append((group_name, subgroup, index))

            for subvalue, sublabel in choices:
                selected = (not has_selected or self.allow_multiple_selected) and str(
                    subvalue
                ) in value
                has_selected |= selected
                subgroup.append(
                    self.create_option(
                        name,
                        subvalue,
                        sublabel,
                        selected,
                        index,
                        subindex=subindex,
                        attrs=attrs,
                    )
                )
                if subindex is not None:
                    subindex += 1
        return groups

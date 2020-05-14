# -*- coding: utf-8 -*-
# Copyright (c) 2013 by Pablo Martín <goinnn@gmail.com>
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

if sys.version_info[0] == 2:
    string = basestring  # noqa: F821
    string_type = unicode  # noqa: F821
else:
    string = str
    string_type = string


def get_max_length(choices, max_length, default=200):
    if max_length is None:
        if choices:
            return len(','.join([string_type(key) for key, label in choices]))
        else:
            return default
    return max_length


def add_other_field_in_choices(choices):
    _choices = choices

    if isinstance(_choices, dict):
        _choices = _choices.items()

    if 'other' not in [c for c, _ in _choices]:
        if isinstance(choices, tuple):
            return choices + (('other', 'Other'),)
        if isinstance(choices, list):
            return choices + [('other', 'Other')]
        if isinstance(choices, dict):
            choices['other'] = 'Other'
            return choices

    return choices


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

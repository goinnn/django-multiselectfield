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
# along with this programe.  If not, see <https://www.gnu.org/licenses/>.


from django.core import validators
from django.utils.translation import gettext_lazy as _


class MaxValueMultiFieldValidator(validators.MaxLengthValidator):
    code = 'max_multifield_value'

    def clean(self, x):
        return len(','.join(x))


class MinChoicesValidator(validators.MinLengthValidator):
    message = _('You must select a minimum of  %(limit_value)d choices.')
    code = 'min_choices'


class MaxChoicesValidator(validators.MaxLengthValidator):
    message = _('You must select a maximum of  %(limit_value)d choices.')
    code = 'max_choices'

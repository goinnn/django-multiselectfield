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


class MSFList(list):

    def __init__(self, choices, *args, **kwargs):
        self.choices = choices
        super(MSFList, self).__init__(*args, **kwargs)

    def __str__(msgl):
        msg_list = [msgl.choices.get(int(i)) if i.isdigit() else msgl.choices.get(i) for i in msgl]
        return ', '.join([str(s) for s in msg_list])


def get_max_length(choices, max_length, default=200):
    if max_length is None:
        if choices:
            return len(','.join([str(key) for key, label in choices]))
        else:
            return default
    return max_length

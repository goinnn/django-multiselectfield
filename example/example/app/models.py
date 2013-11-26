# -*- coding: utf-8 -*-
# Copyright (c) 2013 by Pablo Martín <goinnn@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models

from multiselectfield import MultiSelectField

CATEGORY_CHOICES = (
    (1, 'Handbooks and manuals by discipline'),
    (2, 'Business books2'),
    (3, 'Books of literary criticism'),
    (4, 'Books about literary theory'),
    (5, 'Books about literature')
)

TAGS_CHOICES = (
    ('sex', 'Sex'),
    ('work', 'Work'),
    ('happy', 'Happy'),
    ('food', 'Food'),
    ('field', 'Field'),
    ('boring', 'Boring'),
    ('interesting', 'Interesting'),
    ('huge', 'huge'),
    ('nice', 'Nice'),
)


class Book(models.Model):
    title = models.CharField(max_length=200)
    categories = MultiSelectField(choices=CATEGORY_CHOICES,
                                  max_choices=3)
    tags = MultiSelectField(choices=TAGS_CHOICES,
                            null=True, blank=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.__str__()

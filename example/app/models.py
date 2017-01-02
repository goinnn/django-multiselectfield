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
from django.utils.translation import gettext as _

from multiselectfield import MultiSelectField

CATEGORY_CHOICES = (
    (1, _('Handbooks and manuals by discipline')),
    (2, _('Business books')),
    (3, _('Books of literary criticism')),
    (4, _('Books about literary theory')),
    (5, _('Books about literature')),
)

TAGS_CHOICES = (
    ('sex',         _('Sex')),          # noqa: E241
    ('work',        _('Work')),         # noqa: E241
    ('happy',       _('Happy')),        # noqa: E241
    ('food',        _('Food')),         # noqa: E241
    ('field',       _('Field')),        # noqa: E241
    ('boring',      _('Boring')),       # noqa: E241
    ('interesting', _('Interesting')),  # noqa: E241
    ('huge',        _('Huge')),         # noqa: E241
    ('nice',        _('Nice')),         # noqa: E241
)

PROVINCES = (
    ('AB', _("Alberta")),
    ('BC', _("British Columbia")),
)

STATES = (
    ('AK', _("Alaska")),
    ('AL', _("Alabama")),
    ('AZ', _("Arizona")),
)

PROVINCES_AND_STATES = (
    (_("Canada - Provinces"), PROVINCES),
    (_("USA - States"),       STATES),  # noqa: E241
)


class Book(models.Model):
    title = models.CharField(max_length=200)
    categories = MultiSelectField(choices=CATEGORY_CHOICES,
                                  max_choices=3,
                                  # default='1,5')
                                  default=1)
    tags = MultiSelectField(choices=TAGS_CHOICES,
                            null=True, blank=True)
    published_in = MultiSelectField(_("Province or State"),
                                    choices=PROVINCES_AND_STATES,
                                    max_choices=2)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.__str__()

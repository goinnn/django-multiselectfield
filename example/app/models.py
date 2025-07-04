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
# along with this software.  If not, see <https://www.gnu.org/licenses/>.

from django.db import models
from django.utils.translation import gettext_lazy as _

from multiselectfield import MultiSelectField, SortMultiSelectField


ONE = '1'
TWO = '2'
THREE = '3'
FOUR = '4'
FIVE = '5'


CATEGORY_CHOICES = (
    (ONE, _('Handbooks and manuals by discipline')),
    (TWO, _('Business books')),
    (THREE, _('Books of literary criticism')),
    (FOUR, _('Books about literary theory')),
    (FIVE, _('Books about literature')),
)


CHAPTER_CHOICES = (
    (ONE, 'Chapter I'),
    (TWO, 'Chapter II'),
    (THREE, 'Chapter III'),
)

TAGS_CHOICES = [
    ('sex',         _('Sex')),          # noqa: E241
    ('work',        _('Work')),         # noqa: E241
    ('happy',       _('Happy')),        # noqa: E241
    ('food',        _('Food')),         # noqa: E241
    ('field',       _('Field')),        # noqa: E241
    ('boring',      _('Boring')),       # noqa: E241
    ('interesting', _('Interesting')),  # noqa: E241
    ('huge',        _('Huge')),         # noqa: E241
    ('nice',        _('Nice')),         # noqa: E241
]

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
    title = models.CharField(_('title'), max_length=200)
    categories = MultiSelectField(_('categories'), choices=CATEGORY_CHOICES, max_choices=3, default=[ONE, FIVE])
    tags = MultiSelectField(_('tags'), choices=TAGS_CHOICES, blank=True)
    favorite_tags = SortMultiSelectField(_('favorite tags'), choices=TAGS_CHOICES, blank=True, max_choices=2)
    published_in = MultiSelectField(_("province or state"), choices=PROVINCES_AND_STATES, max_choices=2)
    chapters = MultiSelectField(_("chapters"), choices=CHAPTER_CHOICES, default=[ONE], min_choices=2)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.__str__()

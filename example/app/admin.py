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

from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext as _

from .models import Book


def _multiple_choice_filter(field_name, label):

    class MultiSelectFilter(admin.SimpleListFilter):
        title = label
        parameter_name = field_name

        def lookups(self, request, model_admin):
            return model_admin.model._meta.get_field(field_name).flatchoices

        def queryset(self, request, queryset):
            value = self.value()
            if value:
                queryset = queryset.filter(Q(**{
                    f'{self.parameter_name}__exact': value,
                }) | Q(**{
                    f'{self.parameter_name}__startswith': f'{value},',
                }) | Q(**{
                    f'{self.parameter_name}__endswith': f',{value}'
                }) | Q(**{
                    f'{self.parameter_name}__icontains': f',{value},'
                }))

            return queryset
    return MultiSelectFilter


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'categories', 'tags', 'published_in')
    list_filter = (
        _multiple_choice_filter('categories', _('categories')),
        _multiple_choice_filter('tags', _('tags')),
        _multiple_choice_filter('favorite_tags', _('favourite tags')),
        _multiple_choice_filter('published_in', _('province or state')),
        _multiple_choice_filter('chapters', _('chapters')),
    )

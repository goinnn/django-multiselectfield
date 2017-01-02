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

from django import VERSION
from django.conf import settings
try:
    from django.conf.urls import include, url

    # Compatibility for Django > 1.8
    def patterns(prefix, *args):
        if VERSION < (1, 9):
            from django.conf.urls import patterns as django_patterns
            return django_patterns(prefix, *args)
        elif prefix != '':
            raise NotImplementedError("You need to update your URLConf for "
                                      "Django 1.10, or tweak it to remove the "
                                      "prefix parameter")
        else:
            return list(args)
except ImportError:  # Django < 1.4
    from django.conf.urls.defaults import include, patterns, url

from django.contrib import admin
from django.views.static import serve

admin.autodiscover()

js_info_dict = {
    'packages': ('django.conf',),
}

urlpatterns = patterns(
    '',
    url(r'^', include('app.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns(
    '',
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
        serve,
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)

# -*- coding: utf-8 -*-
# Copyright (c) 2012-2013 by Pablo Martín <goinnn@gmail.com>
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

# Initial code got from http://djangosnippets.org/users/danielroseman/

import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="django-multiselectfield",
    version="0.0.3",
    author="Daniel Roseman and Pablo Martin",
    author_email="goinnn@gmail.com",
    description="Django multiple select field",
    long_description=(read('README.rst') + '\n\n' + read('CHANGES.rst')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    license="LGPL 3",
    keywords="django,multiple,select,field,choices",
    url='https://github.com/goinnn/django-multiselectfield',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
)

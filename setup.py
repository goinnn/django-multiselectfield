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

# Initial code inspired by https://djangosnippets.org/users/danielroseman/

import codecs
import os

from setuptools import find_packages, setup


def read(*rnames):
    with codecs.open(
        os.path.join(os.path.dirname(__file__), *rnames),
        'r', 'utf-8',
    ) as f:
        return f.read()


setup(
    name="django-multiselectfield",
    version="1.0.1",
    author="Pablo Martin",
    author_email="goinnn@gmail.com",
    description="Django multiple select field",
    long_description=(read('README.rst') + '\n\n' + read('CHANGES.rst')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Framework :: Django :: 5.1',
    ],
    license="LGPL 3",
    keywords="django,multiple,select,field,choices",
    url='https://github.com/goinnn/django-multiselectfield',
    packages=find_packages(),
    include_package_data=True,
    tests_require=[
        'django>=3.2',
        'tox',
        'coverage',
        'flake8',
    ],
    install_requires=[
        'django>=3.2',
    ],
    zip_safe=False,
)

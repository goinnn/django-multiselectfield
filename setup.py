#http://djangosnippets.org/users/danielroseman/
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="django-multiselectfield",
    version="0.0.1",
    author="Daniel Roseman",
    author_email="goinnn@gmail.com",
    description="Django multiple select field",
    long_description=(read('README.rst') + '\n\n' + read('CHANGES.rst')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    ],
    license="LGPL 3",
    keywords="django,multiple,select,field,choices",
    url='https://github.com/goinnn/django-multiselectfield',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
)

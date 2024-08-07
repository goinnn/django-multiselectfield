Changelog
=========

0.1.13 (2024-06-30)
-------------------

* Return MSFList instead of a plain list from form fields (`#118 <https://github.com/goinnn/django-multiselectfield/pull/118>`_, `#135 <https://github.com/goinnn/django-multiselectfield/pull/135>`_)
* Fix CI (`#122 <https://github.com/goinnn/django-multiselectfield/pull/122>`_, `#147 <https://github.com/goinnn/django-multiselectfield/pull/147>`_, `#148 <https://github.com/goinnn/django-multiselectfield/pull/148>`_, `#151 <https://github.com/goinnn/django-multiselectfield/pull/151>`_)
* Add ``min_choices`` to defaults when converting to form field (`#123 <https://github.com/goinnn/django-multiselectfield/pull/123>`_)
* Django 5.0 support and remove old compatibility (`#148 <https://github.com/goinnn/django-multiselectfield/pull/148>`_)

Thanks to:

* `tomasgarzon <https://github.com/tomasgarzon>`_
* `aleh-rymasheuski <https://github.com/aleh-rymasheuski>`_
* `nametkin <https://github.com/nametkin>`_
* `karolyi <https://github.com/karolyi>`_
* `olivierdalang <https://github.com/olivierdalang>`_
* `PetrDlouhy <https://github.com/PetrDlouhy>`_

0.1.12 (2020-02-20)
-------------------

* Optimize multiselectfield to_python method
* Thanks to:
    * `daimon99  <https://github.com/daimon99>`_

0.1.11 (2019-12-19)
-------------------

* Added support for Django 3
* Added support for Python 3.8
* Thanks to:
    * `thijsBoehme  <https://github.com/thijsBoehme>`_

0.1.9 (2019-10-02)
------------------

* Added support for Django 2
* Added support for Python 3.6
* Drop support for Python (2.6, 3.3)
* Thanks to:
    * `hirokinko <https://github.com/hirokinko>`_

0.1.6 (2017-05-10)
------------------

* Added support for Django 1.11
* Added support for Python 3.6
* Improved rendering in Django admin
* Improved documentation
* Thanks to:
    * `atten <https://github.com/atten>`_
    * `ixc <https://github.comixc>`_
    * `LeilaniAnn <https://github.comLeilaniAnn>`_

0.1.5 (2017-01-02)
------------------

* Added support for Django 1.8-1.10
* Added support for named groups in choices
* Added support for min_choices argument
* Various fixes
* More tests
* Thanks to:
    * `danilogbotelho <https://github.comdanilogbotelho>`_
    * `dmitry-krasilnikov <https://github.comdmitry-krasilnikov>`_
    * `Kamil Dębowski <https://github.comkdebowski>`_

0.1.4 (2016-02-23)
------------------

* Fixed warning about SubfieldBase
* Added support for Django 1.8+
* Added support for named groups
* We now play nice with django-dynamic-fixture
* More tests

0.1.3 (2014-10-13)
------------------

* Support to Django 1.7 (I'm sorry to the delay)
* Adding get_FIELD_list function
* Fix an error when a MultiSelectField was reandonly at the admin site
* Thanks to:
    * `Hernil <https://github.com/hernil>`_
    * `Vasyl Stanislavchuk <https://github.com/vasyabigi>`_
    * `Litchfield <https://github.com/litchfield/>`_
    * `Chris-erickson <https://github.com/chris-erickson>`_

0.1.2 (2014-04-04)
------------------

* Include the spanish translations to the pypi egg
* Improvements in the readme file
* Windows OS compatibility
* Thanks to:
    * `StillNewb <https://github.com/StillNewb>`_
    * `Diego Yungh <https://github.com/DiegoYungh>`_

0.1.1 (2013-12-04)
------------------
* Move the multiselectfield app to parent folder
* Details

0.1.0 (2013-11-30)
------------------

* Test/example project
* Now works if the first composant of the list of tuple is an integer
* Now max_length is not required, the Multiselect field calculate it automatically.
* The max_choices attr can be a attr in the model field
* Refactor the code
* Spanish translations
* Support to python2.6
* Thanks to:
    * `Daniele Procida <https://github.com/evildmp>`_

0.0.3 (2013-09-11)
------------------

* Python 3 compatible
* Fix an error, the snippet had another error when the choices were translatables
* Improvements in the README file


0.0.2 (2012-09-28)
------------------

* Fix an error, the snippet had an error.

0.0.1 (2012-09-27)
------------------

* Initial version from the next `snippet <https://djangosnippets.org/snippets/1200/>`_

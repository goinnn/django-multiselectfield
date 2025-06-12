1.0.1 (2025-06-12)
-------------------

* Badge image worked on GitHub but was broken on PyPI — fixed it.

1.0.0 (2025-06-12)
-------------------

This release introduces multiple changes that are incompatible with previous versions.

The major version number has been incremented following `Semantic Versioning (SemVer) <https://semver.org/>`_, as several components of the package have changed in ways that may require updates in client code.

The internal codebase has been significantly cleaned up and reorganized, making it more maintainable and consistent.

This version contains **40% fewer lines of code** compared to the previous release.

Less code means fewer bugs, easier maintenance, and better long-term sustainability.


* Breaking changes

    * Remove MSFList (`01dcad230dc368b88a39bfc36f90ddd145f381a2 <https://github.com/goinnn/django-multiselectfield/commit/01dcad230dc368b88a39bfc36f90ddd145f381a2>`_):

        * Removed: (`50d3f785883e0a314f2dc89950e3fe1e88a7ede6 <https://github.com/goinnn/django-multiselectfield/commit/50d3f785883e0a314f2dc89950e3fe1e88a7ede6>`_)
        * It was created to support MultiSelectFields in admin.list_display, but it never actually worked. If you add a multiselect field to list_display, Django does not call to __str__ method of MSGList (renamed to MSFList)
        * It was created for integer choices too and it is a misconception. This is explained in the README file.

    * Remove MSFFlatchoices (`01dcad230dc368b88a39bfc36f90ddd145f381a2 <https://github.com/goinnn/django-multiselectfield/commit/01dcad230dc368b88a39bfc36f90ddd145f381a2>`_):

        * Removed: (`5638247c1d70670d4f81adf35143ef17a7d7575e <https://github.com/goinnn/django-multiselectfield/commit/5638247c1d70670d4f81adf35143ef17a7d7575e>`_)
        * In list_display, labels for the choices are now shown (comma-separated) instead of the values of the choices (comma-separated).

    * In to_python method, value is a list or a string. (`c4579138dda2833cbce26afbf57da5353aa45690 <https://github.com/goinnn/django-multiselectfield/commit/c4579138dda2833cbce26afbf57da5353aa45690>`_)

        * Remove set case and dict case
        * If this breaks something, please create a test to help understand the use case.

    * Removing integer choices:

        * It was a mistake. MultiSelectField inherits of CharField, not IntegerField.
        * It is impossible knows if original choice is (1, 'Item title 2.1') or ('1', 'Item title 2.1')


* Fix: Form instance generated twice since Django  (`#168 <https://github.com/goinnn/django-multiselectfield/pull/168>`_)

* Fix CSS admin:

    *  (`#173 <https://github.com/goinnn/django-multiselectfield/pull/173>`_)
    *  (`7711f4aa755c81d00f07ce8a6ff0fd9240061f9c <https://github.com/goinnn/django-multiselectfield/commit/7711f4aa755c81d00f07ce8a6ff0fd9240061f9c>`_)

* Fix Properly Display Categorized Choices in get_FOO_display (`#169 <https://github.com/goinnn/django-multiselectfield/pull/169>`_)

* SortMultiSelectField: (`#172 <https://github.com/goinnn/django-multiselectfield/pull/172>`_)

* Documentation:

    * How to add a filter to the Django administration:

        * (`e36cbae4c3b39dac4a3fee03fdda9622a101f22d <https://github.com/goinnn/django-multiselectfield/commit/e36cbae4c3b39dac4a3fee03fdda9622a101f22d>`_)
        * Inspired by (`#116 <https://github.com/goinnn/django-multiselectfield/issues/116>`_)

    * How add a django multiselect field to list_display in Django administration

        * (`5638247c1d70670d4f81adf35143ef17a7d7575e <https://github.com/goinnn/django-multiselectfield/commit/5638247c1d70670d4f81adf35143ef17a7d7575e>`_)


    * How to add support for read-only fields in the Django administration:

        * (`65376239ae7491414f896adb4d314349ff7c2667 <https://github.com/goinnn/django-multiselectfield/commit/65376239ae7491414f896adb4d314349ff7c2667>`_)

* Cleanup: Removed outdated code and updated compatibility:

    * Updated syntax for the targeted Python and Django versions. (`#161 <https://github.com/goinnn/django-multiselectfield/pull/161>`_)

    * Add pre-commit hooks (`#161 <https://github.com/goinnn/django-multiselectfield/pull/161>`_)

    * Fixed GitHub Actions workflow.

    * Removed Travis CI configuration.

    * Fix Coveralls integrations

    * Improved the README: clarified the correct versions of Python and Django.


Thanks to:

* `mikemanger <https://github.com/mikemanger>`_
* `piranhaphish <https://github.com/piranhaphish>`_
* `kunalgrover05 <https://github.com/kunalgrover05>`_
* `royatkup <https://github.com/royatkup>`_
* `qasimgulzar <https://github.com/qasimgulzar>`_
* `austin-schick <https://github.com/austin-schick>`_
* `Pfizer-BradleyBare <https://github.com/Pfizer-BradleyBare>`_
* `SuperSandro2000 <https://github.com/SuperSandro2000>`_
* `jucajuca <https://github.com/jucajuca>`_
* `filipefigcorreia <https://github.com/filipefigcorreia>`_
* `ZippoLag <https://github.com/ZippoLag>`_
* `leifdenby <https://github.com/leifdenby>`_
* `jordanvs <https://github.com/jordanvs>`_
* `hetdev <https://github.com/hetdev>`_
* `blag <https://github.com/blag>`_

Special thanks to:

* `ccalero <https://github.com/ccalero>`_ for fighting and updating django-multiselectfield
* `Joinup Green Intelligence <https://joinup.es>`_ for believing in free (libre) software

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

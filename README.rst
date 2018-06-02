django-randomslugfield
======================

.. image:: https://travis-ci.org/mkrjhnsn/django-randomslugfield.svg?branch=master
    :target: https://travis-ci.org/mkrjhnsn/django-randomslugfield
.. image:: https://img.shields.io/pypi/v/django-randomslugfield.svg
    :target: https://pypi.python.org/pypi/django-randomslugfield/
.. image:: https://img.shields.io/pypi/dm/django-randomslugfield.svg
    :target: https://pypi.python.org/pypi/django-randomslugfield/

Django field that automatically generates random slugs.

e.g. example.com/kEwD58P

Tested with Python 2.7, 3.3+ and Django 1.4+.


Getting it
----------

To install django-randomslugfield:

.. code:: bash

    $ pip install django-randomslugfield


Install
-------

To enable ``randomslugfield`` in your project you need to add it to
``INSTALLED_APPS`` in your projects ``settings.py`` file:

.. code:: python

    INSTALLED_APPS = (
        ...
        'randomslugfield',
        ...
    )


Usage
-----

Import ``RandomSlugField`` and use it in your model:

.. code:: python

    from django.db import models
    from randomslugfield import RandomSlugField

    class MyModel(models.Model):
        slug = RandomSlugField(length=7)

The ``length`` argument is required.


Advanced Usage
--------------

By default randomslugfield generates its slug using these characters:

``abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789``

You can optionally exclude lowercase/uppercase/digits/vowels using
``exclude_lower=True``, ``exclude_upper=True``, ``exclude_digits=True``,
``exclude_vowels=True``.

You cannot exclude all characters.

Example:

.. code:: python

    class MyModel(models.Model):
        slug = RandomSlugField(length=7, exclude_lower=True)

The total number of unique slugs is determined by ``characters^length``.

::

    62^9 = 13,537,086,546,263,552 possible slugs
    62^8 = 218,340,105,584,896 possible slugs
    62^7 = 3,521,614,606,208 possible slugs
    62^6 = 56,800,235,584 possible slugs
    62^5 = 916,132,832 possible slugs

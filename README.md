Django Functest Generator
===========================

## What it does

This is a simple script that inspects a django urls.py file and
generates skeleton unittest.TestCase tests which use the django test
Client to simulate GET requests to each URL.  Keyword arguments for
each URL are derived from the urls.py

It is really just to save you some typing and remove one excuse for
not testing all your views.

It writes them to stdout; just redirect to a file and edit as needed.

Usage:

    export DJANGO_SETTINGS_MODULE=foo.settings
    django_functest_generator.py app_name > tests.py


This will look for urls in app_name.urls.


## What it doesn't do

Doesn't (yet) work with un-named URLs.

Doesn't (yet) generate anything other than GET requests.

It's not configurable or tweakable; it just does what it does, and you
do the rest by editing the output.

It doesn't try to generate *valid* kwargs for URLs: it uses 'test' as
the value for every arg. You'll need to edit those; on many URL
regexes, the generated tests will fail with a NoReverseMatch error.

It doesn't generate unit tests, only functional tests.
(See eg. http://carljm.github.com/django-testing-slides/ about the differences)

It doesn't think.  These "tests" are really just skeletons or stubs
for you to edit or replace to get a real test. *Always think about
what you're really testing*.  As one trivial example, this assumes
that every GET request should have a 200 response.


## TODO

* Make it into a django-admin.py command?

* Proper arg parsing  and --help support

* Make it a package and put it on pypi

* Customize output via templates or something?

* Option to use RequestFactory instead of Client?

* or try django-webtest?

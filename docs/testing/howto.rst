==================
Running unit tests
==================


Using a virtualenv
------------------

You can use ``virtualenv`` to test without polluting your system's Python environment.

1. Install ``virtualenv``::

    $ pip install virtualenv

2. Create and activate a ``virtualenv``::

    $ cd thecut-publishing
    $ virtualenv .
    $ source bin/activate
    (thecut-publishing) $

3. Manually link to thecut requirements.
    In python 3 we have issues with package namespaces being shared between site-packages
    and the local directory. So we need to link manually. You will need to manually clone
    the following package and checkout master
    thecut-authorship
    (thecut-publishing) $ cd thecut
    (thecut-publishing) $ ln -s ~/thecut-authorship/thecut/authorship .
    (thecut-publishing) $ cd ..

4. Install the test suite requirements::

    (thecut-publishing) $ pip install -r requirements-test.txt

5. Ensure a version of Django is installed::

    (thecut-publishing) $ pip install "Django>=1.8,<1.9"

6. Run the test runner::

    (thecut-publishing) $ python runtests.py

7. Run the tests with coverage
    coverage run --branch --omit=lib/*,/home/mark/thecut-ordering/*,/home/mark/thecut-publishing/*,/home/mark/thecut-authorship/*,thecut/menus/migrations/* runtests.py
    coverage report -m

Using tox
---------------------------------

You can use tox to automatically test the application on a number of different
Python and Django versions.

1. Install ``tox``::

    $ pip install -r requirements-test.txt

2. Run ``tox``::

    (thecut-publishing) $ tox --recreate

Tox assumes that a number of different Python versions are available on your
system. If you do not have all required versions of Python installed on your
system, running the tests will fail. See ``tox.ini`` for a list of Python
versions that are used during testing.

Test coverage
-------------

The included ``tox`` configuration automatically detects test code coverage with ``coverage``::

      $ coverage report

============
pygitversion
============

**A set of plugins for setuptools_scm to enable better version tracking**

.. start-badges

.. image:: https://api.travis-ci.org/RadioAstronomySoftwareGroup/pygitversion.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/RadioAstronomySoftwareGroup/pygitversion

.. image:: https://coveralls.io/repos/RadioAstronomySoftwareGroup/pygitversion/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/RadioAstronomySoftwareGroup/pygitversion

.. end-badges

Installation
============

::

    pip install pygitversion

Usage
=====
The usage is almost exactly the same as using `setuptools_scm <https://pypi.org/project/setuptools-scm/>`_,
so follow those guidelines. This package merely adds a couple of plugin functions to make the
versioning a bit better (eg. having the branch name in the version if applicable).

To summarise: create a ``pyproject.toml`` and include (at least) the following lines::

    # pyproject.toml
    [build-system]
    requires = ["setuptools>=30.3.0", "wheel", "setuptools_scm", "pygitversion"]

Then in your ``setup.py``, add the following to the call to ``setup()``::

    # setup.py
    from setuptools import setup
    from pygitversion import branch_scheme

    setup(
        ...
        use_scm_version={
            "local_scheme": branch_scheme
        },
    )

You can now print the version of the package simply by doing::

    $ python setup.py --version

To set the version of your code, make your ``__init__.py`` have the following::

    from pkg_resources import get_distribution, DistributionNotFound
    try:
        __version__ = get_distribution(__name__).version
    except DistributionNotFound:
        # package is not installed
        pass

And that's it!


Development
===========

To run the all tests run::

    tox


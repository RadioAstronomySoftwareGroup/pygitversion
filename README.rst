============
pygitversion
============

**Robustly generate exact git hashes for python packages**

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis|
        | |coveralls|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |travis| image:: https://api.travis-ci.org/RadioAstronomySoftwareGroup/pygitversion.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/RadioAstronomySoftwareGroup/pygitversion

.. |coveralls| image:: https://coveralls.io/repos/RadioAstronomySoftwareGroup/pygitversion/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/RadioAstronomySoftwareGroup/pygitversion

.. |version| image:: https://img.shields.io/pypi/v/pygitversion.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/pygitversion

.. |commits-since| image:: https://img.shields.io/github/commits-since/RadioAstronomySoftwareGroup/pygitversion/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/RadioAstronomySoftwareGroup/pygitversion/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/pygitversion.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/pygitversion

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pygitversion.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pygitversion

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pygitversion.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/pygitversion


.. end-badges

Installation
============

::

    pip install pygitversion

Usage
=====
The point of pygitversion is to enable you to robustly create your package with exact
git version information, rather than *just* a simple version specifier.

It does *not replace* the semantic version specifier of your package, but rather
complements it. pygitversion provides the tools necessary to *always* have git
information available in a Python package (whether the actual repo is available or
not).

To use in your package, follow these steps:

1. If ``pyproject.toml`` does not exist in your package, create it.
2. Add the key ``[build-system]`` to ``pyproject.toml``, and add
   ``requires = ['pygitversion>=0.1.6','setuptools>40.8.0','wheel']`` to the key.
3. Ensure that ``__init__.py`` contains the correct semantic ``__version__`` specifier
   (eg. `__version__ = 0.1.0`).
4. In `setup.py`, add the following::

       import pygitversion
       pygitversion.write_git_info_file(__file__, <rel_path_to_package>)

5. Ensure the package has a ``MANIFEST.in``, and that it includes at least::

       include <package>/GIT_INFO

6. The git version of the module may then be accessed inside your package by doing::

    import pygitversion
    pygitversion.construct_version_info(my_package_name)

7. It is recommended (but not necessary) that ``__init__.py`` contain::

    import pygitversion
    GIT_VERSION = pygitversion.construct_version_info(__name__)

8. It is also recommended to add ``GIT_INFO`` to your ``.gitignore``.

Cases Addressed
---------------
There are various ways a package can be installed, and ``pygitversion`` attempts to ensure
that in each case, the git version is available. The following assumes the above
steps have been followed in your package.

1. Package cloned and installed via ``pip install .``: a ``GIT_INFO`` file is created and
   installed due to ``MANIFEST.in``. That ``GIT_INFO`` file is found whenever the package
   is loaded. **This will break iff the installed files on your PYTHONPATH are directly
   modified, which should never be the case.**
2. Package cloned and installed via ``pip install -e .``: the module that is imported
   refers to the actual git repo (via symlink), and the git info is created at import
   time directly from the repo. This still works if the code is updated in place.
3. Package installed directly from hosted source control via ``pip install git+git:...``:
   When pip installs the package, it first fully clones the repo, which means the GIT_INFO
   file is built and added to the install, just as in point 1.
4. Package installed from PyPI (``pip install <package>``): the process of building the
   sdist and bdist to upload to PyPI inherently re-builds and bundles the ``GIT_INFO``
   file as part of the build, and this is installed with the package. Developers should
   be careful to build/upload only clean repositories.


Development
===========

To run the all tests run::

    tox


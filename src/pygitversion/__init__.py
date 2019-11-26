# -*- mode: python; coding: utf-8 -*
# Copyright (c) 2019 Radio Astronomy Software Group
# Licensed under the 2-clause BSD License
from __future__ import absolute_import, division, print_function

import json
import os
import subprocess
import sys
import re
import io

from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass


def get_py_major_version():
    """Return the (int) major Python version currently being used."""
    version_info = sys.version_info
    return version_info[0]


def _unicode_to_str(u):
    """If using Python 2, convert unicode to str"""
    if get_py_major_version() == 2:
        return u.encode("utf8")
    return u


def _get_git_output(args, dir, capture_stderr=False):
    """Get output from Git, ensuring that it is of the ``str`` type,
    not bytes.

    Parameters
    ----------
    args : list of str
        List og arguments to pass to `git -c <dir>`
    dir : str
        Filepath to package directory
    capture_stderr : bool, optional
        Whether to redirect stderr to stdout

    Returns
    -------
    str : stdout output of `git -C <dir> <args>`
    """

    argv = ["git", "-C", dir] + args

    if capture_stderr:
        data = subprocess.check_output(argv, stderr=subprocess.STDOUT)
    else:
        data = subprocess.check_output(argv)

    data = data.strip()

    if get_py_major_version() == 2:
        return data
    return data.decode("utf8")


def _get_package_dir(package):
    """Return the package directory"""
    if type(package) is str:
        return os.path.dirname(package)
    else:
        try:
            dir = os.path.dirname(os.path.realpath(getattr(package, "__file__")))
        except AttributeError:
            raise ValueError(
                "'package' must be a string name to a package, or an actual package"
            )
        return dir


def _get_gitinfo_file(git_file=None, package=None):
    """Get saved info from GIT_INFO file that was created when installing package"""
    if git_file is None:
        if package is None:
            raise ValueError(
                "You must pass either an explicit git_file or a package name"
            )
        else:
            dir = _get_package_dir(package)
            git_file = os.path.join(dir, "GIT_INFO")

    with open(git_file) as data_file:
        data = [_unicode_to_str(x) for x in json.loads(data_file.read().strip())]
        git_origin = data[0]
        git_hash = data[1]
        git_description = data[2]
        git_branch = data[3]

    return {
        "git_origin": git_origin,
        "git_hash": git_hash,
        "git_description": git_description,
        "git_branch": git_branch,
    }


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8"),
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def construct_version_info(package):
    """
    Get full version information, including git details

    Parameters
    ----------
    package : str or imported package
        Either the imported package itself, or the absolute path to the package on
        disk.

    Returns
    -------
    dict
        dictionary giving full version information
    """
    try:
        version = package.__version__
        package_path = package.__file__
    except AttributeError:
        try:
            # Assume its a module that's in the namespace.
            version = sys.modules[package].__version__
            package_path = sys.modules[package].__file__
        except KeyError:
            # package is a *path* to a package.
            init = os.path.join(package, "__init__.py")
            version = find_version(init)
            package_path = os.path.join(package, "__init__.py")

    version_info = {
        "version": version,
        "git_origin": "",
        "git_hash": "",
        "git_description": "",
        "git_branch": "",
    }

    try:
        # First try to ascertain the actual top-level project path.
        project_path = _get_git_output(
            ["rev-parse", "--show-toplevel"],
            dir=os.path.dirname(package_path),
            capture_stderr=True,
        )
    except subprocess.CalledProcessError:
        # The package is not in a git repo -- it must be installed.
        try:
            # Check if a GIT_INFO file was created when installing package
            version_info.update(_get_gitinfo_file(package=package))
        except (IOError, OSError):
            pass

        return version_info

    version_info["git_origin"] = _get_git_output(
        ["config", "--get", "remote.origin.url"], dir=project_path, capture_stderr=True
    )
    version_info["git_hash"] = _get_git_output(
        ["rev-parse", "HEAD"], dir=project_path, capture_stderr=True
    )
    version_info["git_description"] = _get_git_output(
        ["describe", "--dirty", "--tag", "--always"], dir=project_path
    )
    version_info["git_branch"] = _get_git_output(
        ["rev-parse", "--abbrev-ref", "HEAD"], dir=project_path, capture_stderr=True
    )

    return version_info


def write_git_info_file(project_path, package_path):
    """
    Write a GIT_INFO file into a package.

    This function should generally be used in a setup.py file.

    Parameters
    ----------
    package : str
        The name of the package into which to write.
    setup_file : str
        The absolute path to the setup.py file for the project to write to.
    pth : str, optional
        Any extra sub-directories between setup.py and the actual python package (eg src)
    """
    if not os.path.isabs(package_path):
        package_path = os.path.join(project_path, package_path)

    version = construct_version_info(package_path)

    data = [
        version["git_origin"],
        version["git_hash"],
        version["git_description"],
        version["git_branch"],
    ]
    print(version, package_path)

    # Write GIT_INFO to the *package* path (not the project path).
    with open(os.path.join(package_path, "GIT_INFO"), "w") as outfile:
        json.dump(data, outfile)

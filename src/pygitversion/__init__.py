# -*- mode: python; coding: utf-8 -*
# Copyright (c) 2019 Radio Astronomy Software Group
# Licensed under the 2-clause BSD License
from __future__ import absolute_import, division, print_function

import importlib
import json
import os
import subprocess
import sys

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


def _get_package(package):
    try:
        package = importlib.import_module(package)
    except AttributeError:  # assume package is already an actual module
        pass

    return package


def _get_package_dir(package):
    """Return the package directory (i.e. path to import)"""
    package = _get_package(package)

    try:
        dir = os.path.dirname(os.path.realpath(getattr(package, "__file__")))
    except AttributeError:
        raise ValueError(
            "'package' must be a string name to a " "package, or an actual package"
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


def construct_version_info(package):
    """
    Get full version information, including git details

    Parameters
    ----------
    version_file : str, optional
        Full path to a Must be given if `package` not given.
    Returns
    -------
    dict
        dictionary giving full version information
    """
    package = _get_package(package)
    dir = _get_package_dir(package)
    version = package.__version__

    version_info = {
        "version": version,
        "git_origin": "",
        "git_hash": "",
        "git_description": "",
        "git_branch": "",
    }

    try:
        git_origin = _get_git_output(
            ["config", "--get", "remote.origin.url"], dir=dir, capture_stderr=True
        )
        version_info["git_origin"] = git_origin
        version_info["git_hash"] = _get_git_output(
            ["rev-parse", "HEAD"], dir=dir, capture_stderr=True
        )
        version_info["git_description"] = _get_git_output(
            ["describe", "--dirty", "--tag", "--always"], dir=dir
        )
        version_info["git_branch"] = _get_git_output(
            ["rev-parse", "--abbrev-ref", "HEAD"], dir=dir, capture_stderr=True
        )
    except (subprocess.CalledProcessError, ValueError, OSError):  # pragma: no cover
        try:
            # Check if a GIT_INFO file was created when installing package
            version_info.update(_get_gitinfo_file(package=package))
        except (IOError, OSError):
            pass

    return version_info


def write_git_info_file(package):
    version = construct_version_info(package)
    dir = _get_package_dir(package)
    data = [
        version["git_origin"],
        version["git_hash"],
        version["git_description"],
        version["git_branch"],
        dir,
    ]
    print(version, dir, data)

    with open("/home/steven/Documents/GIT_INFO", "w") as outfile:
        json.dump(data, outfile)

    with open(os.path.join(dir, "GIT_INFO"), "w") as outfile:
        json.dump(data, outfile)

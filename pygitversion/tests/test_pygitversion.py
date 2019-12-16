# -*- mode: python; coding: utf-8 -*
# Copyright (c) 2018 Radio Astronomy Software Group
# Licensed under the 2-clause BSD License

"""Tests for version.py.

"""
from pygitversion import branch_scheme
from setuptools_scm.config import Configuration
from setuptools_scm.version import format_version, meta


c = Configuration()


# c.local_scheme = branch_scheme


def test_branch_there():
    v = meta("0.1.0", config=c, branch="branch", distance=1, node="aaaaaaa")
    out = format_version(v, local_scheme=branch_scheme, version_scheme="guess-next-dev")

    assert out == "0.1.1.dev1+aaaaaaa.branch"


def test_no_branch_there():
    v = meta("0.1.0", config=c, branch="branch", distance=None)
    out = format_version(v, local_scheme=branch_scheme, version_scheme="guess-next-dev")

    assert out == "0.1.0"


def test_branch_master():
    v = meta("0.1.0", config=c, branch="master", distance=1, node="aaaaaaa")
    out = format_version(v, local_scheme=branch_scheme, version_scheme="guess-next-dev")

    assert out == "0.1.1.dev1+aaaaaaa"

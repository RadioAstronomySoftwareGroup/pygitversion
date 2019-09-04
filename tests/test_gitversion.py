# -*- mode: python; coding: utf-8 -*
# Copyright (c) 2018 Radio Astronomy Software Group
# Licensed under the 2-clause BSD License

"""Tests for version.py.

"""
from __future__ import absolute_import, division, print_function

import json

import pygitversion as pgv


def test_get_package():
    _pgv = pgv._get_package("pygitversion")
    assert _pgv is pgv

    _pgv = pgv._get_package(pgv)
    assert _pgv is pgv


def test_get_package_dir():
    dir = pgv._get_package_dir("pygitversion")
    assert dir.endswith("pygitversion")


def test_get_gitinfo_file(tmpdir):
    # write a file to read in
    git_file = tmpdir.mkdir("sub").join("GIT_INFO")
    version_info = pgv.construct_version_info(pgv)
    data = [
        version_info["git_origin"],
        version_info["git_origin"],
        version_info["git_origin"],
        version_info["git_origin"],
    ]
    with open(git_file, "w") as outfile:
        json.dump(data, outfile)

    with open(git_file) as data_file:
        data = [pgv._unicode_to_str(x) for x in json.loads(data_file.read().strip())]
        git_origin = data[0]
        git_hash = data[1]
        git_description = data[2]
        git_branch = data[3]

    test_file_info = {
        "git_origin": git_origin,
        "git_hash": git_hash,
        "git_description": git_description,
        "git_branch": git_branch,
    }

    file_info = pgv._get_gitinfo_file(git_file=git_file)

    assert file_info == test_file_info

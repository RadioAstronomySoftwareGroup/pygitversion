# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sphinx_py3doc_enhanced_theme


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.ifconfig",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]
if os.getenv("SPELLCHECK"):
    extensions += ("sphinxcontrib.spelling",)
    spelling_show_suggestions = True
    spelling_lang = "en_US"

source_suffix = ".rst"
master_doc = "index"
project = "pygitversion"
year = "2019"
author = "Radio Astronomy Software Group"
copyright = "{0}, {1}".format(year, author)
version = release = "0.1.0"

pygments_style = "trac"
templates_path = ["."]
extlinks = {
    "issue": (
        "https://github.com/RadioAstronomySoftwareGroup/pygitversion/issues/%s",
        "#",
    ),
    "pr": (
        "https://github.com/RadioAstronomySoftwareGroup/pygitversion/pull/%s",
        "PR #",
    ),
}

html_theme = "sphinx_py3doc_enhanced_theme"
html_theme_path = [sphinx_py3doc_enhanced_theme.get_html_theme_path()]
html_theme_options = {
    "githuburl": "https://github.com/RadioAstronomySoftwareGroup/pygitversion/"
}

html_use_smartypants = True
html_last_updated_fmt = "%b %d, %Y"
html_split_index = False
html_sidebars = {"**": ["searchbox.html", "globaltoc.html", "sourcelink.html"]}
html_short_title = "%s-%s" % (project, version)

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False
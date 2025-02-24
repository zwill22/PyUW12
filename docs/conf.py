import textwrap

project = "PyUW12"
copyright = "2025, Z M Williams"
author = "Z M Williams"
release = "0.1.0"

extensions = [
    "myst_parser",
    "autoapi.extension",
    "sphinx_rtd_theme",
    "breathe",
    "exhale"
]
autoapi_dirs = ["../pyuw12"]


breathe_projects = {"libuw12interface": "./_doxygen/xml/"}
breathe_default_project = "libuw12interface"

exhale_args = {
    "containmentFolder": "./api",
    "rootFileName": "library_root.rst",
    "doxygenStripFromPath": "..",
    "rootFileTitle": "libuw12 interface API",
    "createTreeView": True,
    "exhaleExecutesDoxygen": True,
    "verboseBuild": True,
    "exhaleDoxygenStdin": textwrap.dedent("""
    INPUT = ../src
    PROJECT_NAME = "libuw12interface"
    FILE_PATTERNS = *.cpp
    """),
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

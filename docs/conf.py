import os
import sys

# Do not touch these. They allow the use of the local PRAWdditions.
sys.path.insert(0, ".")
sys.path.insert(1, "..")

from prawdditions import __version__


copyright = "2020, PokestarFan"
exclude_patterns = ["_build"]
extensions = ["sphinx.ext.autodoc", "sphinx.ext.intersphinx"]
html_static_path = ["_static"]
html_theme = "sphinx_rtd_theme"
html_theme_options = {"collapse_navigation": True}
htmlhelp_basename = "PRAWdditions"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3.8", None),
    "praw": ("https://praw.readthedocs.io/en/latest", None),
}
master_doc = "index"
nitpicky = True
project = "PRAWdditions"
pygments_style = "sphinx"
release = __version__
source_suffix = ".rst"
suppress_warnings = ["image.nonlocal_uri"]
version = ".".join(__version__.split(".", 2)[:2])


# Use RTD theme locally
if not os.environ.get("READTHEDOCS"):
    import sphinx_rtd_theme

    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]


def setup(app):
    app.add_stylesheet("theme_override.css")

"""**templating** contains the logic for expanding a Pinecurses template
into data structures parseable by the **parsing** module using **jinja2**."""
from jinja2 import Environment, FileSystemLoader

def expand_pinecurses_template(template_filename):
    """Reads a Pinecurses template and expands dynamic content.
    This is the first step, parsing is the next step (see **parsing**)."""
    pass

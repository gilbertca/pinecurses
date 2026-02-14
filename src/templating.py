"""**templating** contains the logic for expanding a Pinecurses template
into data structures parseable by the **parsing** module using **jinja2**."""
from jinja2 import Environment, FileSystemLoader, select_autoescape

class PinecursesTemplater:
    def __init__(self, template_directory):
        self.environment = Environment(
            loader=FileSystemLoader(template_directory),
            autoescape=select_autoescape()
        )

    def expand_pinecurses_template(
            self,
            template_filename,
            **context
        ):
        """Reads a Pinecurses template and expands dynamic content.
        This is the first step, parsing is the next step (see **parsing**)."""
        template = self.environment.get_template(template_filename)
        return template.render(context)


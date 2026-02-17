"""**pinecurses** contains the primary class: PinecursesApp.

A hypothetical user simply needs to:
    1. Create an html template that defines their app's structure
    2. Create a namespace that links the names and classes
    from their template file to their custom data and functions
    3. Instantiate a PinecursesApp with the template directory and namespace
    4. Call the `run` function, and let Pinecurses do the heavy-lifting
"""
import curses

from dataclasses import dataclass

from src.parsing import PinecursesParser
from src.templating import PinecursesTemplater
from src.keys import PinecursesKeys

class PinecursesApp(
    PinecursesParser,
    PinecursesTemplater,
    PinecursesKeys
):
    def __init__(
        self,
        template_root_file,
        template_directory,
        function_namespace = {},
        template_context = {},
        parser_options = {},
        keys_namespace = {}
    ):
        self.template_root_file = template_root_file # First rendered template
        self.function_namespace = function_namespace # For dynamic text
        self.RUNNING = False # Application status
        PinecursesTemplater.__init__(
            self, 
            template_directory, 
            template_context
        )
        PinecursesParser.__init__(
            self,
            parser_options
        )
        PinecursesKeys.__init__(
            self,
            keys_namespace
        )

    def run(self):
        # Expand the root template:
        expanded_template = (
            self.expand_pinecurses_template(self.template_root_file)
        )

        # Parse tags from root template:
        self.tags = self.parse_pinecurses_config(expanded_template)

        # Enter the main loop:
        return curses.wrapper(self._run)

    def _run(self, stdscr):
        # Initial setup
        self.RUNNING = True
        self.NEEDS_RENDERING = True

        # Expand root template:
        expanded_root_template = self.expand_pinecurses_template(
            self.template_root_file
        )

        # Parse elements from root template:
        parsed_elements = self.parse_elements_from_template(
            expanded_root_template)
        )

        # Main loop
        while self.RUNNING:
            # Draw elements:
            self.render(parsed_elements)

            # Get input from the user:
            self.delegate_key_press()

            # TODO: NEED TO CREATE A WINDOW MANAGER

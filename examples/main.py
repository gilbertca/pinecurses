from src.pinecurses import PinecursesApp as PA

def main() -> int:
    """The main function that an imaginary user might create.
    Useful for testing.

    Returns: an integer status code with the following values:
    - 0 - success
    """
    # Define your namespace for interactivity:
    def hello_world():
        """The simplest widget returns static text."""
        return "Hello, world!"
    function_namespace = {
        "hello_word", hello_world
    }

    # Define where your templates live:
    template_root_dir = "templates"
    template_root_file = "templates/config.xml"

    # Define the context for your templates:
    template_context = {
        "hello_world_button_title": "Hello, world!"
    }

    # TODO: WE NEED AN INTERFACE TO MODIFY CONTEXT AND NAMESPACE DYNAMICALLY

    # Create and run your app:
    app = PA(
        template_root_file,
        template_root_dir,
        template_context,
        function_namespace
    )
    return_value = app.run()

    # Return a friendly error code:
    return return_value


if __name__=="__main__":
    main()

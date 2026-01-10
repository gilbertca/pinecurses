from pinecurses import PinecursesApp as PA


def main() -> int:
    """The main function that an imaginary user might create.
    Useful for testing.

    Returns: an integer status code with the following values:
    - 0 - success
    """
    # Define your namespace:
    def hello_world():
        """The simplest widget returns static text."""
        return "Hello, world!"
    NAMESPACE = {"hello_word", hello_world}

    # Define where your config lives:
    TEST_FILE = "config.html"

    # Create and run your app:
    app = PA(filename=TEST_FILE, function_namespace=NAMESPACE)
    app.run()

    # Return a friendly error code:
    return 0


if __name__=="__main__":
    main()

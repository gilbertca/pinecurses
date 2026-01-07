from parsing import Parser

TEST_FILE = "config.html"
def main() -> int:
    """The main function that an imaginary user might create.
    Useful for testing.

    Returns: an integer status code with the following values:
    - 0 - success
    - 1 - failure
    """
    parser = Parser(TEST_FILE)
    print(parser.soup.find_all('text')[0].prettify())
    return 0

if __name__=="__main__":
    main()

import string


class GeneratorOptions:
    def __init__(self, seed_words):
        """

        :param seed_words: list of seed words for the generator
        :type seed_words: string[]
        """


class Generator:
    """
    Access point for the themed word generator
    """

    def __init__(self):
        self.options = None

    def set_options(self, options: GeneratorOptions) -> None:
        """
        Set the seed words to be used by the generator
        :param options: Options for the word generator
        :return: None
        """
        self.options = options

    def generate_list(self) -> list[string]:
        """

        :return: List of generated words
        """

import string

from model.data import Associations, combine_associations
from tools.api_functions import call_api


class GeneratorOptions:
    """
    Class to store the options for a word generation
    """

    def __init__(self):
        self.__seed_words = []

    @property
    def seed_words(self) -> list[string]:
        """
        List of seed words for the word generator.
        The generations words will result from the associations of all seed words.
        """
        return self.__seed_words

    @seed_words.setter
    def seed_words(self, seed_words: list[string]):
        self.__seed_words = seed_words

    def __eq__(self, other):
        if not isinstance(other, GeneratorOptions):
            return False

        return self.seed_words == other.seed_words


class Generator:
    """
    Access point for the themed word generator
    """

    def __init__(self):
        self.__options = None
        self.__result = None

    def set_options(self, options: GeneratorOptions) -> None:
        """
        Set the options to be used in the next word generation
        :param options: Options for the word generator
        :return: None
        """
        if not options == self.__options:
            self.__options = options
            self.__result = None

    def generate_list(self) -> list[string]:
        """
        Get a plain list of all words associated to any seed word, sorted by their total association score.
        ie. if a word is related to more than one seed word, its score will be the sum of its association scores.
        :return: List of generated words
        """
        if not self.__options:
            print("Can't generate words - no options set.")
            return

        related_words: Associations = Associations()
        for word in self.__options.seed_words:
            combine_associations(related_words, call_api(word))

        self.__result = sorted(related_words, key=related_words.get, reverse=True)
        return self.__result

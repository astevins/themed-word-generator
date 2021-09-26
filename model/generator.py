import string
from enum import Enum
import random

from model.data import Associations, combine_associations
from tools.api_functions import call_api


class AssociationLevel(Enum):
    """
    Represents possible filters on association levels for generator results.
    The higher the score of an associated word, the higher its association level.

    Where n is the number of seed words provided:
        HIGH: score > 50 * n
        MODERATE: 50 * n >= score > 25 * n
        LOW: 25 * m >= score > 10 * n
    """
    HIGH = 1
    MODERATE = 2
    LOW = 3
    HIGHMODERATE = 4
    MODERATELOW = 5
    ALL = 6


class GeneratorOptions:
    """
    Class to store the options for a word generation
    """

    def __init__(self):
        self.__seed_words: list[string] = []
        self.__association_level: AssociationLevel = AssociationLevel.ALL
        self.__num_rand_words: int = 0

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

    @property
    def num_rand_words(self) -> int:
        """
        Number of random words to return within the generated list (including filters)
        If zero, returns all words.
        """
        return self.__num_rand_words

    @num_rand_words.setter
    def num_rand_words(self, num_rand_words: int):
        self.__num_rand_words = num_rand_words

    @property
    def association_level(self) -> AssociationLevel:
        """
        Association level at which to filter the generator results.
        eg. at Association Level HIGH, only high association words will be returned.
        """
        return self.__association_level

    @association_level.setter
    def association_level(self, association_level: AssociationLevel):
        self.__association_level = association_level

    def __eq__(self, other):
        if not isinstance(other, GeneratorOptions):
            return False

        return self.seed_words == other.seed_words and self.association_level == other.association_level


class Generator:
    """
    Access point for the themed word generator
    """

    def __init__(self):
        self.__options: GeneratorOptions = GeneratorOptions()
        self.__result: Associations = Associations()
        self.__unfiltered_result: Associations = Associations()

    def set_options(self, options: GeneratorOptions) -> None:
        """
        Set the options to be used in the next word generation
        :param options: Options for the word generator
        :return: None
        """
        if options.seed_words == self.__options.seed_words:
            return
        if options.seed_words == self.__options.seed_words:
            self.__options = options
            self.__result = None
        else:
            self.__options = options
            self.__result = None
            self.__unfiltered_result = None

    def generate_random_word(self) -> string:
        self.__generate_list()
        return random.choice(list(self.__result.items()))

    def generate_words(self) -> Associations:
        """
        Get a list of words associated to any seed word, sorted by their total association score.
        Will return a random subset of words if num_rand_words is not zero, otherwise will return the entire list.
        Will filter the list by associations scores according to association_level option.
        ie. if a word is related to more than one seed word, its score will be the sum of its association scores.
        :return: List of generated word associations.
                 This is a dict where the keys are the associated words, and the values
                 represent each word's association score.
        """
        self.__generate_list()

        if self.__options.num_rand_words == 0:
            return self.__result
        else:
            result: Associations = Associations()
            i = self.__options.num_rand_words
            while i > 0:
                (new_key, new_value) = random.choice(list(self.__result.items()))
                if new_key not in result.keys():
                    result[new_key] = new_value
                    i -= 1

            return result

    def __generate_list(self) -> None:
        if self.__result or self.__unfiltered_result:
            return

        if not self.__options:
            print("Can't generate words - no options set.")
            self.__result = []
            return

        related_words: Associations = Associations()
        for word in self.__options.seed_words:
            combine_associations(related_words, call_api(word))

        self.__unfiltered_result = self.__sort_associations_by_value(related_words)
        self.__filter_results()

    def __filter_results(self):
        level = self.__options.association_level
        n = len(self.__options.seed_words)
        high_threshold = 100 + 10 * n
        moderate_threshold = 80 + 5 * n
        low_threshold = 60 + 3 * n

        if level == AssociationLevel.ALL:
            self.__result = self.__unfiltered_result
        elif level == AssociationLevel.HIGH:
            self.__result = self.__filter_results_by_score(self.__unfiltered_result, min_score=high_threshold)
        elif level == AssociationLevel.HIGHMODERATE:
            self.__result = self.__filter_results_by_score(self.__unfiltered_result, min_score=moderate_threshold)
        elif level == AssociationLevel.MODERATE:
            self.__result = self.__filter_results_by_score(self.__unfiltered_result,
                                                           min_score=moderate_threshold, max_score=high_threshold)
        elif level == AssociationLevel.MODERATELOW:
            self.__result = self.__filter_results_by_score(self.__unfiltered_result, min_score=low_threshold,
                                                           max_score=high_threshold)
        elif level == AssociationLevel.LOW:
            self.__result = self.__filter_results_by_score(self.__unfiltered_result, min_score=low_threshold,
                                                           max_score=moderate_threshold)

    def __filter_results_by_score(self, associations: Associations, max_score=None, min_score=None) -> Associations:
        """
        Filters an association list to only associations within a certain range of scores.
        :param max_score: Maximum score a word can have to match the filter
        :param min_score: Minimum score a word can have to match the filter
        :return: Associations list filtered by given range of scores
        """
        return {key: value for (key, value) in associations.items() if
                ((not max_score) or value <= max_score) and ((not min_score) or value >= min_score)}

    def __sort_associations_by_value(self, associations: Associations) -> Associations:
        sorted_keys = sorted(associations, key=associations.get, reverse=True)
        sorted_associations = Associations()

        for key in sorted_keys:
            sorted_associations[key] = associations[key]

        return sorted_associations

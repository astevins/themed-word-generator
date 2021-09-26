from model.generator import GeneratorOptions, Generator, AssociationLevel


class Cli(object):
    """
    Command line interface for the themed word generator program
    """

    __SEED_INPUT_PROMPT = "Enter the list of seed words (separated by commas): "
    __FILTER_INPUT_PROMPT = "Enter the association level filter: \n " \
                            "HIGH = 1 \n MODERATE = 2 \n LOW = 3 \n " \
                          "HIGH & MODERATE = 4 \n MODERATE & LOW = 5 \n ALL = 6"
    __NUM_RAND_WORDS_INPUT = "Enter the number of words to generate (or 0 to return all words)"

    def __init__(self):
        self.generator_options = GeneratorOptions()
        self.generator = Generator()

    def run(self):
        self.__get_input_words()
        self.__get_filter_level()
        self.__get_num_rand_words()
        self.generator.set_options(self.generator_options)
        result = self.generator.generate_words()
        print(result)

    def __get_input_words(self):
        print(self.__SEED_INPUT_PROMPT)
        seed_words = input()
        self.generator_options.seed_words = seed_words.split(',')

    def __get_filter_level(self):
        print(self.__FILTER_INPUT_PROMPT)
        association_level_filter: AssociationLevel = AssociationLevel(int(input()))
        self.generator_options.association_level = association_level_filter

    def __get_num_rand_words(self):
        print(self.__NUM_RAND_WORDS_INPUT)
        self.generator_options.num_rand_words = int(input())

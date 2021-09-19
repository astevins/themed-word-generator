from model.generator import *


class Cli(object):
    """
    Command line interface for the themed word generator program
    """

    __SEED_INPUT_PROMPT = "Enter the list of seed words (separated by commas)"

    def __init__(self):
        self.generator = Generator()

    def run(self):
        self.__get_input_words()

    def __get_input_words(self):
        seed_words = input(self.__SEED_INPUT_PROMPT)

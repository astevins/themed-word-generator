from model.generator import GeneratorOptions, Generator


class Cli(object):
    """
    Command line interface for the themed word generator program
    """

    __SEED_INPUT_PROMPT = "Enter the list of seed words (separated by commas): "

    def __init__(self):
        self.generator_options = GeneratorOptions()
        self.generator = Generator()

    def run(self):
        self.__get_input_words()
        self.generator.set_options(self.generator_options)
        result = self.generator.generate_list()
        print(result)

    def __get_input_words(self):
        print(self.__SEED_INPUT_PROMPT)
        seed_words = input()
        self.generator_options.seed_words = seed_words.split(',')

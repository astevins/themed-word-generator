"""
Classes for modeling the data used in this program, and associated functions.
"""

"""
Typed dict stores word associations data from api call
key: word - the associated word
value: scores - scored how closely the associated word is related to the reference word
"""
Associations = dict[str, float]


def combine_associations(dict1: Associations, dict2: Associations) -> Associations:
    """
    Combines associations by summing the scores of words in two Associations dictionaries
    eg. dict1: {'apple': 20, 'core': 10}
        dict2: {'core': 30, 'hollow': 5}
        combination: {'apple': 20, 'core': 40, 'hollow': 5}
    :param dict1: The first associations dictionary to be combined
    :param dict2: The second associations dictionary to be combined
    :return: A reference to dict1, which has been combined with dict2
    """
    for word, score in dict2.items():
        if word in dict1:
            dict1[word] += score
        else:
            dict1[word] = score

    return dict1

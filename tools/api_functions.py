"""
Functions for calling the Word Associations api
"""

import os
import string

import requests
from dotenv import load_dotenv

from model.data import Associations

load_dotenv()
API_KEY = os.environ.get("WORD_ASSOCIATIONS_API_KEY")


def call_api(word: string) -> Associations:
    """
    Calls the Word Associations api with the input word and gets the list of related words
    :param word: The word to call the api for
    :return: The response from the api - the list of related words
    """
    url = "https://twinword-word-associations-v1.p.rapidapi.com/associations/"

    payload = f"entry={word}"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-host': "twinword-word-associations-v1.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    return __parse_api_response(response, word)


def __parse_api_response(response: requests.Response, word: string) -> Associations:
    """
    Gets the list of word associations from an api response
    :param response: Response from the api
    :return: Dict of associations from the api response
    """
    if response.status_code == 200:
        res_json = response.json()

        if res_json['result_code'] == '200':
            return res_json['associations_scored']
        else:
            print(f"Failed to get associations for '{word}': {res_json['result_msg']}")
    else:
        print("Failed to fetch response from api")

    return {}

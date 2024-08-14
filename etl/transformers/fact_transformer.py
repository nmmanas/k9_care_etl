from spellchecker import SpellChecker

from .base_transformer import BaseTransformer


class FactTransformer(BaseTransformer):
    def transform(self, data):
        """
        The `transform_data` function in Python simply returns the input data without
        any transformation.

        :param data: The `transform_data` function you provided simply returns the input
        data as it is without any transformation.
        :return: the `transformed_data`, which is a variable holding the same value as
        the input `data`.
        """
        transformed_data = data
        return transformed_data

    def clean_whitespaces(self, data):
        """
        This function removes extra whitespaces from the "fact" field in each dictionary
        within the input data list.

        :param data: The `clean_whitespaces` function takes a list of dictionaries as
        input, where each dictionary has a key "fact" containing a string value. The
        function then removes extra whitespaces from the "fact" values in each
        dictionary by splitting the string into words, joining them back with a single
        space

        :return: The `clean_whitespaces` function returns the `data` after cleaning
        whitespaces in the "fact" field of each item in the data list.
        """
        for fact in data:
            fact["fact"] = " ".join(fact["fact"].split()).strip()
        return data

    def correct_typos(self, data):
        """
        The function corrects typos in a list of facts by using a SpellChecker to
        correct words and maintain capitalization.

        :param data: facts dictionary in following format:
            [
                {
                    "fact": "fact 1",
                    "created_date": "<date>"
                }
            ]
        :return: The `correct_typos` method returns the `data` after correcting any
        typos in the "fact" field of each item in the data. The typos are corrected
        using the `SpellChecker` class, and the corrected words are stored back in the
        "fact" field before returning the updated `data`.
        """
        spell = SpellChecker()

        for fact in data:
            corrected_words = []
            for word in fact["fact"].split():
                # Check if the word is capitalized or in uppercase
                if word.isupper():
                    corrected_word = spell.correction(word).upper()
                elif word[0].isupper():
                    corrected_word = spell.correction(word).capitalize()
                else:
                    corrected_word = spell.correction(word)
                corrected_words.append(corrected_word)

            fact["fact"] = " ".join(corrected_words)
        return data

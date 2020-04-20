import unittest

from utilities.texts import (get_email, get_grams, get_plural, get_singular,
                             get_url, remove_accent, tokenize)


class TextsTest(unittest.TestCase):

    def test_get_email(self) -> None:
        string = "This is a string containign an email.adress@example.com."
        emails = get_email(string=string)
        self.assertEqual(emails, ["email.adress@example.com"])

    def test_tokenise(self) -> None:
        sentence = "This is a sentence composed of words, cool"
        tokens = tokenize(sentence)
        self.assertEqual(tokens, ['This', 'is', 'a', 'sentence', 'composed', 'of', 'words', ',', 'cool'])
        grams = get_grams(tokens, 3)
        grams
import unittest

from utilities.texts import (get_email, get_plural, get_singular,
                             get_url, remove_accent, tokenize)


class TextsTest(unittest.TestCase):

    def test_get_email(self) -> None:
        string = "This is a string containign an email.adress@example.com."
        emails = get_email(string=string)
        self.assertEqual(emails, ["email.adress@example.com"])

    def test_tokenise(self) -> None:
        string = "This is a sentence composed of words, cool"
        tokens = tokenize(string)
        self.assertEqual(tokens, ['This', 'is', 'a', 'sentence', 'composed', 'of', 'words', ',', 'cool'])

    def test_get_url(self) -> None:
        string = "This is a string containing http://tadadata.fr/ an url and https://github.com/MrMimic/working_utilities another."
        urls = get_url(string=string)
        self.assertEqual(len(urls), 2)
        self.assertIn("http://tadadata.fr/", urls)

    def test_remove_accent(self) -> None:
        string = "Ceçi est ùne phrâsé ën françaîs alämbiqué"
        unicode_str = remove_accent(string=string)
        self.assertEqual(unicode_str, "Ceci est une phrase en francais alambique")

    def test_get_plural(self) -> None:
        word = "pamplemousse"
        plural = get_plural(word=word)
        self.assertEqual(plural, "pamplemousses")
        word = "travaux"
        plural = get_plural(word=word)
        self.assertEqual(plural, "travaux")
        word = "naval"
        plural = get_plural(word=word)
        self.assertEqual(plural, "navaux")

    def test_get_singular(self) -> None:
        word = "totaux"
        singular = get_singular(word=word)
        self.assertEqual(singular, "total")
        word = "violettes"
        singular = get_singular(word=word)
        self.assertEqual(singular, "violette")

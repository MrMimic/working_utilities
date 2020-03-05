import re
import unidecode
import itertools
import RegexpTokenizer


class Text(object):
    """
    **Utilities for text processing.**
    """

    def __init__(self):
        pass

    def clean_xml(self, string):
        """
        Clean XML tags from a string

        :param string: The string to look for URLs in
        :type string: str
        :returns: Cleaned string
        :rtype: str
        """
        s = re.sub(r'<xref .*?>(?:<sup>)?[0-9]{1,3}(?:</sup>)?</xref>', '',
                   str(string).replace('\n', ''))
        s = re.sub(r'<.*?>', '', s)
        return str(s)

    def get_url(self, string):
        """
        Extract URLs from a string

        :param string: The string to look for URLs in
        :type string: str
        :returns: URLs list found
        :rtype: list
        """

        urls = re.findall(
            re.compile(
                r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
            ), str(string))
        return urls

    def get_email(self, string):
        """
        Extract emails adresses from a string

        :param string: The string to look for emails in
        :type string: str
        :returns: Emails list found
        :rtype: list
        """

        emails = re.findall(
            r'[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+',
            str(string))
        return emails

    def get_versions(self, string):
        """
        Extract software versions from a string

        :param string: The string to look for versions in
        :type string: str
        :returns: Versions list found
        :rtype: list
        """

        versions = re.findall(r'[0-9]{1,2}\.[0-9]{1,2}\.[0-9a-zA-Z]{1,3}',
                              string)
        if len(versions) > 0:
            return versions
        else:
            return None

    def remove_accent(self, string):
        """
        Remove accents from a string

        :param string: The string to clean
        :type string: str
        :returns: Unaccented string
        :rtype: str
        """

        unaccented_string = unidecode.unidecode(string)
        return unaccented_string

    def get_plural(self, word):
        """
        Get plural from a word in french

        :param string: The word
        :type string: str
        :returns: Plural word
        :rtype: str
        """

        if word.endswith('al'):
            return re.sub(r'al', 'aux', word)
        elif word.endswith('aux'):
            return word
        elif word.endswith('s'):
            return word
        else:
            return '{}s'.format(word)

    def get_singular(self, word):
        """
        Get singular from a word in french

        :param string: The word
        :type string: str
        :returns: Singular word
        :rtype: str
        """

        if word.endswith('s'):
            return re.sub(r's$', '', word)
        elif word.endswith('aux'):
            return re.sub(r'aux$', 'al$', word)
        else:
            return word

    def get_grams(self, tokens, max_n):
        """
        Get all possible ngrams from a list()

        :param tokens: Tokenized text
        :type tokens: list
        :returns: List of grams
        :rtype: list
        """

        grams = []
        for i in list(reversed(range(1, max_n))):
            for gram in list(itertools.combinations(tokens, i)):
                grams.append(gram)
        return grams

    def tokenize(self, string):
        """
        Tokenize a string

        :param string: The string to tokenize
        :type tokens: str
        :returns: List of tokens
        :rtype: list
        """

        tokens = RegexpTokenizer(r'\w\'|\w+|[^\w\s]').tokenize(string)
        return tokens

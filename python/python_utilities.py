#!/usr/bin/env python3
# coding: utf8

# ==============================================================================
# Title: UTILITIES
# Description: Utilities for Bertha.
# Author: Emeric Dynomant
# Contact: emeric.dynomant@omictools.com
# Date: 27/10/2017
# Language release: python 3.5.2
# ==============================================================================
# OmicX, all rights reserved
# https://omictools.com/
# ==============================================================================

# IMPORT
import re
import os
import sys
import json
import time
import gzip
import smtplib
import requests
import itertools
import subprocess
import networkx as nx
import mysql.connector
from ftplib import FTP
from email import encoders
from pymongo import MongoClient
from scipy.stats import shapiro
from nltk import RegexpTokenizer
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class NIH(object):
    """
    NIH's APIs wrapper
    """

    def __init__(self):
        pass

    def pmid_to_pmcid(self, pmid):
        """
        PMID to PMCID conversion
        """
        api_request = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=MELoDiST&email=bertha@omictools.com&format=json&ids={}'.format(
            re.sub(' ', '', str(pmid)))
        json_data = json.loads(requests.get(api_request).text)
        if len(json_data['records']) == 1:  # Check just in case ..
            try:
                return json_data['records'][0]['pmcid']
            except KeyError:
                return None

    def pmcid_to_pmid(self, pmcid):
        api_request = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=MELoDiST&email=bertha@omictools.com&format=json&ids=PMC{}'.format(
            pmcid)
        json_data = json.loads(requests.get(api_request).text)
        if len(json_data['records']) == 1:  # Check just in case ..
            try:
                return json_data['records'][0]['pmid']
            except KeyError:
                return None

    def doi_to_pmid(self, doi):
        api_request = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=MELoDiST&email=bertha@omictools.com&format=json&ids={}'.format(
            doi)
        json_data = json.loads(requests.get(api_request).text)
        try:
            if len(json_data['records']) == 1:  # Check just in case ..
                return json_data['records'][0]['pmid']
        except KeyError:
            return None


class Mongo(object):
    """
    **Utilities for MongoDB processing.**
    """

    def __init__(self):
        pass

    def get_connection(self, host, port, user, password, database,
                       authentication_database):

        uri = 'mongodb://{}:{}@{}:{}'.format(user, password, host, port)
        connection = MongoClient(uri, authSource=authentication_database)
        client = connection[database]
        return client

    def get_connection_via_ssh(ssh_host, ssh_user, ssh_key_path, ssh_port, mongo_host, mongo_user, mongo_password, mongo_port, mongo_database, mongo_auth_database):
        """
        ***Returns a MongoDB connection, reached through an SSH tunnel**
        """
    
        server = SSHTunnelForwarder(  # Create SSH tunnel
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_pkey=ssh_key_path,
            remote_bind_address=(mongo_host, mongo_port))
        server.start()
    
        # Connect Mongo
        uri = 'mongodb://{}:{}@{}:{}'.format(mongo_user, mongo_password, mongo_host, server.local_bind_port)
        client = MongoClient(uri, authSource=mongo_auth_database)
        connection = client[mongo_database]
    
        return server, connection


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
        s = re.sub('<xref .*?>(?:<sup>)?[0-9]{1,3}(?:</sup>)?</xref>', '',
                   str(string).replace('\n', ''))
        s = re.sub('<.*?>', '', s)
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
            '[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+',
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

        versions = re.findall('[0-9]{1,2}\.[0-9]{1,2}\.[0-9a-zA-Z]{1,3}',
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
            return re.sub('al', 'aux', word)
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
            return re.sub('s$', '', word)
        elif word.endswith('aux'):
            return re.sub('aux$', 'al$', word)
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

        tokens = RegexpTokenizer('\w\'|\w+|[^\w\s]').tokenize(string)
        return tokens


class Database(object):
    """
    Database utilities
    """

    def __init__(self,
             user,
             password,
             host,
             database,
             port,
             ssl_ca=None,
             ssl_cert=None,
             ssl_key=None):
        """"""
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.ssl_ca = ssl_ca
        self.ssl_cert = ssl_cert
        self.ssl_key = ssl_key

    def get_connection(self):

        # Configuration
        config = {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'database': self.database,
            'port': self.port,
            'use_pure': True,
            'raise_on_warnings': True,
            'get_warnings': True,
            'autocommit': True
        }

        if self.ssl_ca is not None:
            config['ssl_ca'] = self.ssl_ca
        if self.ssl_key is not None:
            config['ssl_key'] = self.ssl_key
        if self.ssl_cert is not None:
            config['ssl_cert'] = self.ssl_cert

        # Connection
        if sys.version_info.major == 3 and sys.version_info.minor > 4:  # kwargs was not set up before 3.5
            connection = mysql.connector.connect(**config, buffered=True)
        else:
            connection = mysql.connector.connect(
                user=config['user'],
                host=config['host'],
                password=config['password'],
                database=config['database'],
                ssl_ca=config['ssl_ca'],
                ssl_cert=config['ssl_cert'],
                ssl_key=config['ssl_key'])

        return connection


class Stats(object):
    """
    Stats utilities
    """

    def __init__(self):
        pass

    def check_normality(self, serie, alpha=0.05):
        """
        Performs a Shapiro and Wilk test on a serie of value to look for its normality

        :param serie: A list of values
        :type serie: list
        :param alpha: The alpha to compare pvalue
        :type alpha: float
        :returns: Wheter the serie is normal or not
        :rtype: bool
        """

        stat, p = shapiro(serie)
        print('Statistics=%.3f, p=%.3f' % (stat, p))

        if p > alpha:
            return True
        else:
            return False


class Graph(object):
    """
    Directed graph processing
    """

    def __init__(self):
        pass

    def initiate_graph(self, graph_type):
        """
        """
        if graph_type == 'digraph':
            return nx.DiGraph()

    def add_edge(self, graph, source, target, weight):
        """
        """
        graph.add_edge(str(source), str(target), weight=weight)
        return graph

    def get_successors(self, graph, node):
        """
        """
        return [x for x in graph.successors(node)]

    def get_predecessors(self, graph, node):
        """
        """
        return [x for x in graph.predecessors(node)]

    def get_edge_weight(self, graph, source, target):
        """
        """
        weight = graph.get_edge_data(source, target)
        if weight is not None:
            return weight['weight']
        else:
            return None

    def get_possible_starts(self, graph):
        """
        """
        possible_starts = []
        for node in graph.nodes():
            if len(list(graph.predecessors(node))) == 0:
                possible_starts.append(node)
        return possible_starts

    def get_distance(self, node_1, node_2):
        """Get mean distance between two points"""

        path_length = nx.shortest_path_length(
            self.ontology.graph, source=node_1, target=node_2)
        return path_length

    def get_edge_weight(self, graph, source, target):

        try:
            weight = graph.get_edge_data(*(source, target))['weight']
        except KeyError:
            weight = None
        return weight

    def set_edge_weight(self, graph, source, target, weight):

        graph[source][target]['weight'] = weight
        return graph


class Lists(object):
    def __init__(self):
        pass

    def flatten_list(self, list_of_list):
        flat_list = [item for sublist in list_of_list for item in sublist]
        return flat_list

    def remove_outliers(self, X, Y, t=3.5):
        """ Remove outliers from a numerical list X based on z-score > t """

        mean_X = np.mean(X)
        std_X = np.std(X)

        good_x = []
        good_y = []

        for x, y in zip(X, Y):
            z_score = (x - mean_X) / std_X
            if z_score < t:
                good_x.append(x)
                good_y.append(y)
        return good_x, good_y


class Emails(object):
    """
    Work with distant mail services

    :param email: The email to connect to
    :type email: str
    :param password: The associated password
    :type password: str
    :param server: The server to connect
    :type server: str
    :param port: The port used to connect the server
    :type port: int
    """

    def __init__(self, email, password, server, port):

        self.server = smtplib.SMTP(server, port)
        self.server.starttls()
        self.server.login(email, password)

        self.email = email

    def send_mail(self, corresponding, file_name, subject, text):
        """
        Uses server connected into the init to send mails
        
        :param corresponding: List of email to send mail to
        :type corresponding: list
        :param file_name: Path to the file to join
        :type file_name: str / None
        :param text: The text body
        :type text: str
        """

        for adress in corresponding:  # For each address
            # Write mail
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = adress
            msg['Subject'] = subject
            body = text
            msg.attach(MIMEText(body, 'plain'))
            # Add file
            if file_name is not None:
                attachment = open(file_name, 'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename = {}'.format(file_name))
                msg.attach(part)
            # Send
            text = msg.as_string()
            self.server.sendmail(self.email, adress, text)
            self.server.quit()


class Random(object):
    """
    Unclassable shits
    """

    def __init__(self):
        pass

    def get_random_joke(self):
        """
        Just uses an API to get random joke
        """
        url = 'https://icanhazdadjoke.com/'
        header = {'Accept': 'application/json'}
        joke = json.loads(requests.get(url, headers=header).text).get('joke')
        return joke

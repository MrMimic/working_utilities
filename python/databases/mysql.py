import sys

from mysql import connector


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
            connection = connector.connect(**config, buffered=True)
        else:
            connection = connector.connect(
                user=config['user'],
                host=config['host'],
                password=config['password'],
                database=config['database'],
                ssl_ca=config['ssl_ca'],
                ssl_cert=config['ssl_cert'],
                ssl_key=config['ssl_key'])

        return connection

#!/usr/bin/env python3
# coding: utf8

import sys
from typing import Optionnal

from mysql import connector


def get_connection(host: str, user: str, password: str, database: str,
                   port: int, ssl_ca: Optionnal[str], ssl_key: Optionnal[str],
                   ssl_cert: Optionnal[str]) -> connector:
    """
    Reach a MySQL DB, even throu SSL connection.

    Args:
        host (str): DB Host name.
        user (str): DB user.
        password (str): DB user's password.
        database (str): DB name.
        port (int): DB host port.
        ssl_ca (Optionnal[str]): SSL authorization path.
        ssl_key (Optionnal[str]): SSL key path.
        ssl_cert (Optionnal[str]): SSL certificate path.

    Returns:
        connector: Connector linked to the DB.
    """
    # Configuration
    config = {
        'host': host,
        'user': user,
        'password': password,
        'database': database,
        'port': port,
        'use_pure': True,
        'raise_on_warnings': True,
        'get_warnings': True,
        'autocommit': True
    }

    if ssl_ca is not None:
        config['ssl_ca'] = ssl_ca
    if ssl_key is not None:
        config['ssl_key'] = ssl_key
    if ssl_cert is not None:
        config['ssl_cert'] = ssl_cert

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

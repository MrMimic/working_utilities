#!/usr/bin/env python3
# coding: utf8

from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder


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

    def get_connection_via_ssh(self, ssh_host, ssh_user, ssh_key_path, ssh_port, mongo_host, mongo_user, mongo_password, mongo_port, mongo_database, mongo_auth_database):
        """
        Returns a MongoDB connection, reached through an SSH tunnel
        """

        server = SSHTunnelForwarder(  # Create SSH tunnel
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_pkey=ssh_key_path,
            remote_bind_address=(mongo_host, mongo_port))
        server.start()

        # Connect Mongo
        uri = 'mongodb://{}:{}@{}:{}'.format(mongo_user,
                                             mongo_password, mongo_host, server.local_bind_port)
        client = MongoClient(uri, authSource=mongo_auth_database)
        connection = client[mongo_database]

        return server, connection

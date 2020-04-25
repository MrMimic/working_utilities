#!/usr/bin/env python3
# coding: utf8

from typing import Optionnal

from pymongo import MongoClient

from sshtunnel import SSHTunnelForwarder


def get_connection(
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
        authentication_database: Optionnal[str] = None) -> MongoClient:
    """
    Get direct connection to a MongoDB.

    Args:
        host (str): Host name.
        port (int): Host port.
        user (str): User of the DB.
        password (str): User's password.
        database (str): Name of the database.
        authentication_database (str): Optionnal DB conaining users.

    Returns:
        MongoClient: The connection to the DB server.
    """
    uri = 'mongodb://{}:{}@{}:{}'.format(user, password, host, port)
    if authentication_database is not None:
        connection = MongoClient(uri, authSource=authentication_database)
    else:
        connection = MongoClient(uri)
    client = connection[database]
    return client


def get_connection_via_ssh(
        ssh_host: str,
        ssh_user: str,
        ssh_key_path: str,
        ssh_port: int,
        mongo_host: str,
        mongo_user: str,
        mongo_password: str,
        mongo_port: int,
        mongo_database: str,
        mongo_auth_database: Optionnal[str] = None) -> MongoClient:
    """
    Returns a MongoDB connection, reached through an SSH tunnel.

    Args:
        ssh_host (str): SSH host name.
        ssh_user (str): SSH user.
        ssh_key_path (str): SSH key.
        ssh_port (int): SSH port.
        mongo_host (str): DB hostname.
        mongo_user (str): User.
        mongo_password (str): Pass.
        mongo_port (int): Mongo DB port.
        mongo_database (str): Name of the mongo DB.
        mongo_auth_database (Optionnal[str], optional): Auth database. Defaults to None.

    Returns:
        MongoClient: Client to reach the distant DB.
    """
    server = SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_pkey=ssh_key_path,
        remote_bind_address=(mongo_host, mongo_port))
    server.start()
    uri = 'mongodb://{}:{}@{}:{}'.format(mongo_user, mongo_password,
                                         mongo_host, server.local_bind_port)
    client = MongoClient(uri, authSource=mongo_auth_database)
    connection = client[mongo_database]

    return server, connection

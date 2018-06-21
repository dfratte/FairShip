"""@package mongoDb
Database connection class
"""
from mongoengine import connect


class DbConnect(object):
    """
    Class to manage database connection
    """

    @staticmethod
    def get_connection(db_name):
        """
        Create an instance of the database connection.
        :param db_name: The name of the database to connect to.
        """
        connect(
            db=db_name,
            # user=user,
            # password=password,
            host='localhost',
            port=27017
        )

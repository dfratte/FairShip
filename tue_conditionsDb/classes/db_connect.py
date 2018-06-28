"""@package tue_conditionsDb
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

    @staticmethod
    def delete_db(db_name):
        """
        Dalete the database of which name is provided.
        :param db_name: The name of the database to delete.
        """
        db_connect = connect(db_name)
        db_connect.drop_database(db_name)

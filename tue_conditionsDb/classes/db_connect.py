"""@package mongoDb
Database connection class
"""
from mongoengine import connect


class DbConnect(object):
    """
    Class to manage database connection
    """

    @staticmethod
    def get_connection(connection_dict):
        """
        Create an instance of the database connection.
        :param connection_dict: Dict containinig all the information to make a connection.
        """
        connect(
            db=connection_dict['db_name'],
#             user=user,
#             password=password,
            host=connection_dict['host'],
            port=connection_dict['port']
        )

    @staticmethod
    def delete_db(connection_dict):
        """
        Dalete the database of which name is provided.
        :param connection_dict: Dict containinig all the information to make a connection.
        """
        db_connect = connect(
            db=connection_dict['db_name'],
#             user=user,
#             password=password,
            host=connection_dict['host'],
            port=connection_dict['port']
        )
        
        db_connect.drop_database(connection_dict['db_name'])

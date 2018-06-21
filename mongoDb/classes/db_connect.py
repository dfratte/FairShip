"""@package mongoDb
Database connection class
"""
from mongoengine import connect


class DbConnect(object):

    @staticmethod
    def get_connection(db_name):
        connect(
            db=db_name,
            # user=user,
            # password=password,
            host='localhost',
            port=27017
        )

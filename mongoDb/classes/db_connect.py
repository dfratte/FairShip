from mongoengine import *


class DB_connect:
    # variable = "blah"

    def dbname(self, dbname):
        # connect(dbname)

        connect(db=dbname,
                # user=user,
                # password=password,
                host='localhost',
                port=27017
                )
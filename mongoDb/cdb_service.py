"""@package mongoDb
ConditionsDB Command Line Interface
"""
import argparse
import json

from datetime import datetime
from models import Condition
from api import API

HELP_DESC = '''

  #####  ####### ######  #     # 
 #     # #       #     # ##    # 
 #       #       #     # # #   # 
 #       #####   ######  #  #  # 
 #       #       #   #   #   # # 
 #     # #       #    #  #    ## 
  #####  ####### #     # #     # 

Conditions Database Service
FairSHiP 2018

Developed by Eindhoven University of Technology (ST) under some Open Source License

This script is used to retrieve condition data from a condition database.
'''


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f").strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


class Service(object):

    def validate_arguments(self, args):

        list_sd_filter = [x for x in vars(args) if (x != 'list_subdetectors' and vars(args)[x] is not None)]

        flag_ls = len(list_sd_filter) > 1 and args.list_subdetectors is True

        show_cd_filter = [x for x in vars(args) if (x != 'condition' \
                                                    and vars(args)[x] is not None and vars(args)[x] is not False)]

        flag_cd = len(show_cd_filter) == 0 and args.condition is not None

        show_iov_filter = [x for x in vars(args) if (x != 'iov' \
                                                     and vars(args)[x] is not None and vars(args)[x] is not False)]

        flag_iov = len(show_iov_filter) == 0 and args.iov is not None

        add_sub_filter = [x for x in vars(args) if (x != 'new_sub' \
                                                    and vars(args)[x] is not None and vars(args)[x] is not False)]

        flag_add_sub = len(add_sub_filter) != 0 and args.new_sub is not None

        if flag_ls or flag_cd or flag_iov or flag_add_sub:
            return True

        return False

    def run(self, *params):

        api = API()

        parser = argparse.ArgumentParser(description=HELP_DESC, formatter_class=argparse.RawDescriptionHelpFormatter)

        # mutually exclusive group for list subdetectors, show subdetector and add subdetector

        group_lsn = parser.add_mutually_exclusive_group()

        # mutually exclusive group for show condition and show iov

        group_ci = parser.add_mutually_exclusive_group()

        group_lsn.add_argument('-ls', '--list-subdetectors',
                               dest='list_subdetectors',
                               help='Lists all Subdetectors of the Conditions database.',
                               action="store_true")

        group_lsn.add_argument('-ss', '--show-subdetector',
                               dest='subdetector',
                               default=None,
                               required=False,
                               help='Shows all the data related to a specific Subdetector.')

        group_ci.add_argument('-sc', '--show-condition',
                              dest='condition',
                              default=None,
                              required=False,
                              help='Shows a specific Condition of a Subdetector. Search is done by Condition name.')

        group_ci.add_argument('-si', '--show-iov',
                              dest='iov',
                              default=None,
                              required=False,
#                               type=valid_date,
                              help='Retrieves a list of Conditions based on a specific IOV or IOV range.')

        group_lsn.add_argument('-as', '--add-subdetector',
                               dest='new_sub',
                               default=None,
                               required=False,
                               help='Adds a new Subdetector and its Conditions from a path to a JSON file.')

        group_ci.add_argument('-st', '--show-tag',
                            dest='tag',
                            default=None,
                            required=False,
                            help='Retrieves a list of Conditions based on a specific tag.')

        parser.add_argument('-v', '--verbose',
                            dest='verbose',
                            help='Prints out to the console the output of a command.',
                            action="store_true")

        if params:
            args = parser.parse_args(params)
        else:
            args = parser.parse_args()

        #         print vars(args)

        ### Arguments dependencies verification ###

        if self.validate_arguments(args):
            parser.error('arguments error')

        if args.list_subdetectors is True:
            subdetectors = api.list_subdetectors()
            if args.verbose:
                print subdetectors.to_json()
            return subdetectors

        if args.subdetector is not None and args.condition is None and args.iov is None and args.tag is None:
            print "-ss executed"
            subdetector = api.show_subdetector(args.subdetector)
            if args.verbose:
                print subdetector.to_json()
            return subdetector

        if args.subdetector is not None and args.condition is not None:
            print "-sc executed"
            condition = api.show_subdetector_condition(args.subdetector, args.condition)
            if args.verbose:
                print condition.to_json()
            return condition
        
        if args.tag is not None:
            print "-st executed"
            condition = api.show_subdetector_tag(args.subdetector, args.tag)
            if args.verbose:
                if type(condition) is Condition:
                    print condition.to_json()
                else:
                    for i in condition:
                        print i.to_json()
            return condition

        if args.subdetector is not None and args.iov is not None:
            iov = api.show_subdetector_iov(args.subdetector, args.iov)
            if args.verbose:
                if type(iov) is not list:
                    print iov.to_json()
                else:
                    for i in iov:
                        print i.to_json()
            return iov

        if args.new_sub is not None:
            print "-as executed"
            with open(args.new_sub) as loaded_file:
                data = json.load(loaded_file)
                result = api.add_subdetector(data)
                print "Subdetector added successfully!" if (result == 1) else "Error adding new Subdetector"

        return True

if __name__ == '__main__':
    Service().run()
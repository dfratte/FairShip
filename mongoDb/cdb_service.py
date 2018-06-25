"""@package mongoDb
ConditionsDB Command Line Interface
"""
import argparse
import json
import io

from datetime import datetime
from models import Condition
from api import API

HELP_DESC = '''


  #####  ####### ######  #     #             ####### #     #       #        
 #     # #       #     # ##    #                #    #     #      #  ###### 
 #       #       #     # # #   #                #    #     #     #   #      
 #       #####   ######  #  #  #    #####       #    #     #    #    #####  
 #       #       #   #   #   # #                #    #     #   #     #      
 #     # #       #    #  #    ##                #    #     #  #      #      
  #####  ####### #     # #     #                #     #####  #       ###### 
                                                                            
                        Conditions Database Service
                                FairSHiP 2018

Developed by Eindhoven University of Technology under GNU General Public License v3.0

Software Technology PDEng Program
Generation 2017

This script is used to retrieve condition data from a condition database.
'''

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f").strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


class Service(object):

    @staticmethod
    def save(file, data, mode):
        with io.open(file, mode, encoding='utf-8') as f:
            f.write(unicode(data));
            print "Data exported successfully!"
    
    @staticmethod
    def output(data):
        parsed = json.loads(data.to_json())
        print json.dumps(parsed, indent=4, sort_keys=True)

    @staticmethod
    def validate_arguments(args):

        list_sd_filter = [x for x in vars(args) if (x != 'list_subdetectors' and vars(args)[x] is not None)]

        flag_ls = len(list_sd_filter) > 2 and args.list_subdetectors is True

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
        
        parser.add_argument('-f', '--file',
                            dest='output_file',
                            default=None,
                            required=False,
                            help='Redirects the output of a command to a JSON file.')

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
                for idx, s in enumerate(subdetectors):
                    print idx+1,"-", s["name"]
            if args.output_file:
                self.save(args.output_file, subdetectors.to_json(), 'w')
            return subdetectors

        if args.subdetector is not None and args.condition is None and args.iov is None and args.tag is None:
            print "-ss executed"
            subdetector = api.show_subdetector(args.subdetector)
            if args.verbose:
                self.output(subdetector)
            if args.output_file:
                self.save(args.output_file, subdetector.to_json(), 'w')
            return subdetector

        if args.subdetector is not None and args.condition is not None and args.iov is None:
            print "-sc executed"
            condition = api.show_subdetector_condition(args.subdetector, args.condition)
            if args.verbose:
                self.output(condition)
            if args.output_file:
                self.save(args.output_file, condition.to_json(), 'w')
            return condition

        if args.tag is not None:
            print "-st executed"
            condition = api.show_subdetector_tag(args.subdetector, args.tag)
            if isinstance(condition, Condition):
                if args.verbose:
                    self.output(condition)
                if args.output_file:
                    self.save(args.output_file, condition.to_json(), 'w')
            else:
                if args.verbose:
                    for i in condition:
                        self.output(i)
                if args.output_file:
#                     for i in condition:
#                         self.save(args.output_file, i.to_json(), 'a')
                    print "Unsupported data export!"
            return condition

        if args.subdetector is not None and args.iov is not None:
            print "-si executed"
            iov = api.show_subdetector_iov(args.subdetector, args.iov)
            if not isinstance(iov, list):
                if args.verbose:
                    self.output(iov)
                if args.output_file:
                    self.save(args.output_file, iov.to_json(), 'w')
            else:
                if args.verbose:
                    for i in iov:
                        self.output(i)
                if args.output_file:
#                     for i in iov:
#                         self.save(args.output_file, i.to_json(), 'a')
                    print "Unsupported data export!"
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

"""@package mongoDb
ConditionsDB Command Line Interface
"""
import argparse
import io
import json
from datetime import datetime

from api import API
from models import Condition

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

class Service(object):

    def __init__(self):
        self.result = None
        self.is_list = False

    @staticmethod
    def save(file_name, data, mode):
        with io.open(file_name, mode, encoding='utf-8') as f:
            f.write(unicode(data))
            print "Data exported successfully!"

    @staticmethod
    def output(data):
        parsed = json.loads(data.to_json())
        print json.dumps(parsed, indent=4, sort_keys=True)

    def produce_output(self, data, args, is_list):
        if is_list:
            for idx, s in enumerate(data):
                if args.list_subdetectors:
                    print idx + 1, "-", s
                else:
                    Service.output(s)
        else:
            Service.output(data)
            
        if args.output_file:
            if self.is_list:
                print "Unsupported data export."
            else:
                Service.save(args.output_file, data.to_json(), 'w')

    @staticmethod
    def validate_arguments(args):

        list_sd_filter = [x for x in vars(args) if (x != 'list_subdetectors' and vars(args)[x] is not None)]

        flag_ls = len(list_sd_filter) > 2 and args.list_subdetectors is True  # fixme: hardcoded value

        show_cd_filter = [x for x in vars(args) if
                          (x != 'condition' and vars(args)[x] is not None and vars(args)[x] is not False)]

        flag_cd = len(show_cd_filter) == 0 and args.condition is not None

        show_iov_filter = [x for x in vars(args) if
                           (x != 'iov' and vars(args)[x] is not None and vars(args)[x] is not False)]

        flag_iov = len(show_iov_filter) == 0 and args.iov is not None

        add_sub_filter = [x for x in vars(args) if
                          (x != 'new_sub' and vars(args)[x] is not None and vars(args)[x] is not False)]

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
                               help='Lists all Subdetectors from the Conditions database.',
                               action="store_true")
        
        group_lsn.add_argument('-gas', '--get-all-subdetectors',
                               dest='get_all_subdetectors',
                               help='Get all Subdetectors from the Conditions database.',
                               action="store_true")

        group_lsn.add_argument('-ss', '--show-subdetector',
                               dest='subdetector',
                               default=None,
                               required=False,
                               help='Shows all the data related to a specific Subdetector.')
        
        group_lsn.add_argument('-as', '--add-subdetector',
                               dest='new_sub',
                               default=None,
                               required=False,
                               help='Adds a new Subdetector and its Conditions from a path to a JSON file.')
    
        group_lsn.add_argument('-gs', '--get-snapshot',
                               dest='get_snapshot',
                               default=None,
                               required=False,
                               help='Gets a snapshot of Conditions based on a specific date.')

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

        group_ci.add_argument('-st', '--show-tag',
                              dest='tag',
                              default=None,
                              required=False,
                              help='Retrieves a list of Conditions based on a specific tag.')

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

        if self.validate_arguments(args):
            parser.error('arguments error')

        if args.list_subdetectors is True:
            subdetectors_names = api.list_subdetectors()
            self.result = subdetectors_names
            self.is_list = True
            
        if args.get_all_subdetectors is True:
            subdetectors = api.get_all_subdetectors()
            self.result = subdetectors
            self.is_list = True
        
        if args.get_snapshot is not None:
            iov, tag_name = args.get_snapshot.split(" ")
            snapshot = api.get_snapshot(iov, tag_name)
            self.result = snapshot
            self.is_list = True

        if args.subdetector is not None and args.condition is None and args.iov is None and args.tag is None:
            subdetector = api.show_subdetector(args.subdetector)            
            self.result = subdetector

        if args.subdetector is not None and args.condition is not None and args.iov is None:
            condition = api.show_subdetector_condition(args.subdetector, args.condition)
            self.result = condition

        if args.tag is not None:
            condition = api.show_subdetector_tag(args.subdetector, args.tag)
            if not isinstance(condition, Condition):
                self.is_list = True
            self.result = condition

        if args.subdetector is not None and args.iov is not None:
            iov = api.show_subdetector_iov(args.subdetector, args.iov)
            if isinstance(iov, list):
                self.is_list = True
            self.result = iov

        if args.new_sub is not None:
            with open(args.new_sub) as loaded_file:
                data = json.load(loaded_file)
                added = api.add_subdetector(data)
                if added == 1:
                    print "Subdetector added successfully!"
                    return True
                print "Error adding new Subdetector"
                return False

        self.produce_output(self.result, args, self.is_list)
        
        return self.result


if __name__ == '__main__':
    service = Service()
    service.run()

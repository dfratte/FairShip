import argparse
import datetime as date

from api import *

help_desc = '''

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

parser = argparse.ArgumentParser(description=help_desc,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-ls', '--list-subdetectors',
                    dest='list_subdetectors',
                    help='Flag to retrieve all subdetectors of the conditions db',
                    action="store_true")

parser.add_argument('-sd', '--subdetector',
                    dest='subdetector',
                    default=None,
                    required=False,
                    help='Name of the subdetector to retrieve.')

parser.add_argument('-c', '--condition',
                    dest='condition',
                    default=None,
                    required=False,
                    help='Name of the condition to retrieve.')

args = parser.parse_args()

# flag to check that a subdetector exists when querying for a condition
# TODO: move this to an array of flags/error msg and analyze it in a separate function
flag_sd_c1      = vars(args)['list_subdetectors'] is True and vars(args)['subdetector'] is not None and vars(args)['condition'] is not None
flag_sd_c2      = vars(args)['list_subdetectors'] is False and vars(args)['subdetector'] is None and vars(args)['condition'] is not None

list_sd_filter  = filter(lambda x: (x != 'list_subdetectors' and vars(args)[x] is not None), vars(args))
flag_ls         = len(list_sd_filter) != 0 and args.list_subdetectors is True


if (flag_sd_c1 or flag_sd_c2 or flag_ls):
    parser.error('arguments error')

if args.list_subdetectors is True:
    subdetectors = list_subdetectors()
#     print subdetectors.to_json()

if args.subdetector is not None and args.condition is None:
    subdetector = show_subdetector(args.subdetector)
#     print subdetector.to_json()

if args.subdetector is not None and args.condition is not None:
    condition = show_subdetector_condition(args.subdetector, args.condition)
#     print condition.to_json()
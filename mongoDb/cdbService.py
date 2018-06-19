import argparse
import datetime as date

def valid_date(s):
	try:
		return date.datetime.strptime(s, "%Y-%m-%d %H:%M")
	except ValueError:
		msg = "Given Datetime ({0}) not valid! Expected format, 'YYYY-MM-DD HH:mm'!".format(s)
		raise argparse.ArgumentTypeError(msg)

help_desc='''
Conditions Database Service
FairSHiP - CERN 2018

Developed by Eindhoven University of Technology (ST) under some Open Source License

This script is used to retrieve condition data from a condition database.
'''

parser = argparse.ArgumentParser(description=help_desc,
								 formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-lg', '--list-global-tags',
					dest='list_global_tags',
					help='Flag to retrieve all global tags of the conditions db',
					action="store_true")

parser.add_argument('-sd', '--start-datetime',
					dest='start_datetime',
					type=valid_date,
					default=None,
					required=False,
					help='Start datetime in format "YYYY-MM-DD HH:mm"')
					
parser.add_argument('-s', '--search',
					dest='search_string',
					default=None,
					required=False,
					help='String to be searched in Global Tags attributes (Name, Description, Comments)')

args = parser.parse_args()

print args.start_datetime
print args.list_global_tags
print args.search_string


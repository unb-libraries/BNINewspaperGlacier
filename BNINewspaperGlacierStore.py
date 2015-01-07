# !/usr/bin/python
import os
import sys
from optparse import OptionParser
import ConfigParser


def check_options(options, parser):
    if options.config_file is None or not os.path.exists(options.config_file):
        parser.print_help()
        print "\nERROR: Cannot read configuration file! (--config)"
        sys.exit(2)


def init_options():
    option_parser = OptionParser()
    option_parser.add_option(
        "-c", "--config",
        dest="config_file",
        default='',
        help="The config file to process with.",
    )
    (options, args) = option_parser.parse_args()
    check_options(options, option_parser)
    return options

options = init_options()

config_object = ConfigParser.SafeConfigParser()
config = config_object.read(options.config_filepath)

for root, dirs, files in os.walk(config.get('Locations', 'send_to_glacier_path'), topdown=False):
    for name in files:
        print(os.path.join(root, name))
    print "***DIRS***"
    for name in dirs:
        print(os.path.join(root, name))

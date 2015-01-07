# !/usr/bin/python
import os
import sys
from optparse import OptionParser
import ConfigParser
from BNIImageArchiver import BNIImageArchiver

def check_options(options, parser):
  if options.config_filepath is None or not os.path.exists(options.config_filepath):
    parser.print_help()
    print "\nERROR: Cannot read configuration file! (--config)"
    sys.exit(2)


def init_options():
  option_parser = OptionParser()
  option_parser.add_option(
    "-c", "--config",
    dest="config_filepath",
    default='',
    help="The config file to process with.",
  )
  (options, args) = option_parser.parse_args()
  check_options(options, option_parser)
  return options

options = init_options()

config_object = ConfigParser.SafeConfigParser()
config_object.read(options.config_filepath)

top_of_tree = config_object.get('Locations', 'send_to_glacier_path')
shelve_file = config_object.get('Locations', 'shelve_file')
auth_id = config_object.get('AWS', 'key')
auth_key = config_object.get('AWS', 'secret_key')
vault_name = config_object.get('AWS', 'vault_id')

for root, dirs, files in os.walk(top_of_tree, topdown=False):
  for name in files:
    relative_filepath = os.path.join(root,name).replace(top_of_tree + '/', '')
    file_archive = BNIImageArchiver.BNIImageArchiver(top_of_tree, relative_filepath, shelve_file, auth_id, auth_key, vault_name)
    file_archive.archive_file()

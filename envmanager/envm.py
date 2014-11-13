# CLI #
#######

from envmanager.envmanager import EnvManager
import argparse
import os

parser = argparse.ArgumentParser()

# parser.add_argument("filename", 
#                      help="file with paths to envs")
parser.add_argument('-e', '--environment', type=str,
                    help='path to file with paths to envs')
parser.add_argument('-f', '--find', type=str,
                    help='find app, use commas to search for more then one')
parser.add_argument("-l", "--freezelist", action='store_true',
                    help="pints the freeze_ist of all envs")
parser.add_argument("-i", "--install", type = str, 
                    help="installes an app, use commas to add more then one")

args = parser.parse_args()

# print args.filename

if args.environment:
    em = EnvManager(args.environment)
elif os.environ.get('VIRTUAL_ENV'):
    em = EnvManager(env_list=[os.environ['VIRTUAL_ENV']])
else:
    print 'no active virtualenv and no --environment input'
    quit()

if args.find:
    find = []
    arg_input =  args.find
    if ',' in arg_input:
        find += arg_input.split(',')
    else:
        find = arg_input

if args.install:
    install = []
    arg_input =  args.install
    if ',' in arg_input:
        install += arg_input.split(',')
    else:
        install = arg_input



if args.install and args.find:
    em.up(find, install)
elif args.install:
    em.install(install)
elif args.find:
    em.finder(find)

if args.freezelist:
    for n in em.freezeList():
        print n


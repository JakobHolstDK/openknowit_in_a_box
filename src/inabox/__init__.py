from . import inabox

import argparse

def main():
    parser = argparse.ArgumentParser(description="Infrastructure in a box", usage="inabox <action> \n\n \
               \
               version : 0.1.2 BETA \n                                              \
               actions:\n                                                      \
               up         start the IAC \n  \
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup netbox')
    args = parser.parse_args()
    if args.action[0] == 'up':
        print("Starting inabox")
        
    else:
        print("Invalid action. Use --help for more information.")


    
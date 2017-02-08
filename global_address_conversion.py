#!/usr/bin/python
#
#

import sys
import os
import argparse

def main():
    arg_parser = argparse.ArgumentParser( description='Create a global address book for a junos machine')
    arg_parser.add_argument( 'configfile', help='The file containing the configuration.  Can be with or without "display set"' )

    command_line_arguments = arg_parser.parse_args()

    if not os.path.exists( command_line_arguments.configfile ) or not os.path.isfile( command_line_arguments.configfile ):
        # How do I check for input from the command line?  Like a pipe?
        print( 'Cannot open configfile ' + str( command_line_arguments.configfile ), file=sys.stderr )
        sys.exit(1)

    ( usable_file_check, display_set_check ) = detect_junos_config_file_output_type( command_line_arguments.configfile )
    
    if not usable_file_check:
        print( 'Failed to determine JUNOS configuration type', file=sys.stderr )
        sys.exit(1)

    # So now we have a file, wait until we get to the zone declaration part.
    with open( command_line_arguments.configfile, 'r' ) as config_file_handle:
        current_line = config_file_handle.readline()


def detect_junos_config_file_output_type( config_file ):
     # open the file to determine if this is a config with or without display set
     # This is encapsulated in a method so that we can exit early when we detect what we want 
     #        (which will be 99% of cases so why go thru the entire file?
    result_found = False
    display_set_input_file = False
    with open( config_file , 'r' ) as config_file_handle_to_determine_file_type_only:
        while not config_file_handle_to_determine_file_type_only.closed and not result_found:
            current_line = config_file_handle_to_determine_file_type_only.readline() 
            print( 'Checking first 3 characters: "' + current_line[0:3] + '"' )
            print( 'and close boolean evaluates to: ' + str( config_file_handle_to_determine_file_type_only.closed ))
            if current_line[0:3] == 'set':
                result_found = True
                display_set_input_file = True
            elif current_line[-3:] == ' {\n':
                result_found = True
            if result_found:
                return ( result_found, display_set_input_file )

    # If we got here, we did not find the type we wanted :(
    return ( result_found, display_set_input_file )


if __name__ == '__main__':
    main()

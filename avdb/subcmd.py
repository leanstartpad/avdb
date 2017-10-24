# Copyright (c) 2017 Sine Nomine Associates
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THE SOFTWARE IS PROVIDED 'AS IS' AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""Create command line subcommands with argparse

This module provides a thin wrapper over the standard library argparse package
to cleanly create command line subcommands. A decorator turns regular functions
into cli subcommands. The argument function defines command line options.

Example:

    @subcommand(
        argument("host", metavar="<host>", help="example postional option"),
        argument("--filename", "-f", help="example optional flag"),
        argument("--output", default="example", help="example option"),
        )
    def example(args):
        '''example subcommand'''
        print "example"
        print args.host
        print args.filename
        print args.output
        return 0

    dispatch()
    # usage: cli example [options]

# Note: Put trailing underscores on function names to create subcommands
#       which are Python reserved words, such as 'import'.

"""

import argparse

root = argparse.ArgumentParser(description="afs version database")
parent = root.add_subparsers(dest='subcommand')

def subcommand(*args):
    """Decorator to declare command line subcommands."""
    def decorator(function):
        name = function.__name__.strip('_')
        desc = function.__doc__
        parser = parent.add_parser(name, description=desc)
        for arg in args:
            name_or_flags,options = arg
            if 'default' in options and 'help' in options:
                options['help'] += " (default: {})".format(options['default'])
            parser.add_argument(*name_or_flags, **options)
        parser.set_defaults(function=function)
    return decorator

def argument(*name_or_flags, **options):
    """Helper to declare subcommand arguments.

    See argparse add_arguments().
    """
    return (name_or_flags, options)

def summary():
    """Print a summary of the subcommands."""
    print "commands:"
    for name,parser in parent.choices.items():
        print "  %-12s %s" % (name, parser.description)
    return 0

def dispatch():
    """Parse arguments and dispatch subcommand."""
    args = root.parse_args()
    return args.function(args)


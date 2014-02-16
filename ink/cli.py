"""
This module is the commandline interface of ink.

Created on 13 February 2014
@author: Charlie Lewis
"""

import argparse

class main(object):
    """
    This class is responsible for all commandline operations.
    """
    def cli_start(self, args):
        # !! TODO
        print args

    def cli_watch(self, args):
        # !! TODO
        print args

    def cli_unwatch(self, args):
        # !! TODO
        print args

    def cli_list(self, args):
        # !! TODO
        print args

    def parse_args(self):
        parser = argparse.ArgumentParser()

        subparsers = parser.add_subparsers(title='ink commands')

        # start
        parse_start = subparsers.add_parser('start',
                                            help='start the ink service')
        parse_start.add_argument('-D', '--daemon',
                                 help='run as a daemon',
                                 action="store_true",
                                 default=False)
        parse_start.add_argument('-H', '--host',
                                 default="0.0.0.0",
                                 help='specify host to run on')
        parse_start.add_argument('-P', '--port',
                                 type=int, default=3469,
                                 help='specify port to run on')
        parse_start.set_defaults(func=self.cli_start)

        # watch
        parse_watch = subparsers.add_parser('watch',
                                          help='watch a directory')
        parse_watch.add_argument('DIRECTORY',
                                 help='specify directory to watch')
        parse_watch.add_argument('-r', '--recursive',
                                 default=True,
                                 action="store_true",
                                 help='recursively watch a directory')
        parse_watch.add_argument('-m', '--metadata-depth',
                                 type=int, default=1,
                                 help='1=no contents, 2=contents, \
                                       3=external enrichment')
        parse_watch.add_argument('-c', '--cache',
                                 default=None,
                                 help='NONE=pointer to the original file, \
                                       ALL=cache whole file, \
                                       SMART=subset of the metadata and contents')
        parse_watch.set_defaults(func=self.cli_watch)

        # unwatch
        parse_unwatch = subparsers.add_parser('unwatch',
                                          help='stop watching a directory')
        parse_unwatch.add_argument('DIRECTORY',
                                 help='specify directory to stop watching')
        parse_unwatch.set_defaults(func=self.cli_unwatch)

        # list
        parse_list = subparsers.add_parser('list',
                                          help='list directories being watched')
        parse_list.set_defaults(func=self.cli_list)

        args = parser.parse_args()
        args.func(args)

if __name__ == "__main__": # pragma: no cover
    main().parse_args()

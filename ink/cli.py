"""
This module is the commandline interface of ink.

Created on 13 February 2014
@author: Charlie Lewis
"""

import argparse
import redis

class main(object):
    """
    This class is responsible for all commandline operations.
    """
    def __init__(self, redis_host='localhost', redis_port=6379, redis_db=0):
        try:
            self.r = redis.StrictRedis(host=redis_host,
                                       port=redis_port,
                                       db=redis_db)
        except:
            print "Failed to connect to redis, at %s:%s", redis_host, redis_port

    def cli_hosts(self, args):
        # !! TODO
        print args

    def cli_info(self, args):
        # !! TODO
        print args

    def cli_list(self, args):
        # !! TODO
        print args

    def cli_login(self, args):
        # !! TODO
        print args

    def cli_logs(self, args):
        # !! TODO
        print args

    def cli_register(self, args):
        # !! TODO
        print args

    def cli_search(self, args):
        # !! TODO
        print args

    def cli_start(self, args):
        # !! TODO
        # create a file for registration purposes
        # add a new key to the hosts list in redis
        # index known directories for this host
        print args

    def cli_unwatch(self, args):
        # !! TODO
        print args

    def cli_version(self, args):
        # !! TODO
        print args

    def cli_watch(self, args):
        # !! TODO
        print args
        if args.recursive:
            print 1
        print args.DIRECTORY
        # check if this directory is already being watched
        # check if using the same parameters, update if different
        try:
            # !! TODO
            self.r.set("foo",args.DIRECTORY)
        except Exception as e:
            print e
        # !! TODO
        # if the server is already started, index this newly added directory

    def parse_args(self):
        parser = argparse.ArgumentParser()

        subparsers = parser.add_subparsers(title='ink commands')

        # hosts
        parse_hosts = subparsers.add_parser('hosts',
                                            help='list hosts that are registered')
        parse_hosts.set_defaults(func=self.cli_hosts)

        # info
        parse_info = subparsers.add_parser('info',
                                           help='display system-wide information')
        parse_info.set_defaults(func=self.cli_info)

        # list
        parse_list = subparsers.add_parser('list',
                                           help='list directories being watched')
        parse_list.set_defaults(func=self.cli_list)

        # login
        parse_login = subparsers.add_parser('login',
                                            help='login with credentials for \
                                                  access to the index')
        parse_login.add_argument('-e', '--email',
                                 help='email address')
        parse_login.add_argument('-u', '--username',
                                 help='username')
        parse_login.add_argument('PASSWORD',
                                 help='password')
        parse_login.set_defaults(func=self.cli_login)

        # logs
        parse_logs = subparsers.add_parser('logs',
                                           help='server logs')
        parse_logs.add_argument('HOST',
                                default="localhost",
                                help='specify host to get logs from')
        parse_logs.set_defaults(func=self.cli_logs)

        # register
        parse_register = subparsers.add_parser('register',
                                               help='create an account')
        parse_register.add_argument('EMAIL',
                                    help='email address')
        parse_register.add_argument('USERNAME',
                                    help='username')
        parse_register.add_argument('PASSWORD',
                                    help='password')
        parse_register.set_defaults(func=self.cli_register)

        # search
        parse_search = subparsers.add_parser('search',
                                            help='search for files')
        parse_search.set_defaults(func=self.cli_search)
        parse_search.add_argument('QUERY',
                                  help='query')

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

        # unwatch
        parse_unwatch = subparsers.add_parser('unwatch',
                                              help='stop watching a directory')
        parse_unwatch.add_argument('DIRECTORY',
                                   help='specify directory to stop watching')
        parse_unwatch.set_defaults(func=self.cli_unwatch)

        # version
        parse_version = subparsers.add_parser('version',
                                           help='show version')
        parse_version.set_defaults(func=self.cli_version)

        # watch
        parse_watch = subparsers.add_parser('watch',
                                          help='watch a directory')
        parse_watch.add_argument('DIRECTORY',
                                 help='specify directory to watch')
        parse_watch.add_argument('-r', '--recursive',
                                 default=False,
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

        args = parser.parse_args()
        args.func(args)

if __name__ == "__main__": # pragma: no cover
    main().parse_args()

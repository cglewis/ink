"""
This module is the commandline interface of ink.

Created on 13 February 2014
@author: Charlie Lewis
"""

import argparse
import redis
import socket
import sys
from ink.cli_opts import hosts
from ink.cli_opts import info
from ink.cli_opts import list
from ink.cli_opts import login
from ink.cli_opts import logs
from ink.cli_opts import register
from ink.cli_opts import search
from ink.cli_opts import start
from ink.cli_opts import stop
from ink.cli_opts import unwatch
from ink.cli_opts import version
from ink.cli_opts import watch

class cli(object):
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


    def parse_args(self):
        parser = argparse.ArgumentParser()

        subparsers = parser.add_subparsers(title='ink commands')

        # hosts
        parse_hosts = subparsers.add_parser('hosts',
                                            help='list hosts that are registered')
        parse_hosts.set_defaults(func=hosts.hosts.main)

        # info
        parse_info = subparsers.add_parser('info',
                                           help='display system-wide information')
        parse_info.set_defaults(func=info.info.main)

        # list
        parse_list = subparsers.add_parser('list',
                                           help='list directories being watched')
        parse_list.set_defaults(func=list.list.main)

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
        parse_login.set_defaults(func=login.login.main)

        # logs
        parse_logs = subparsers.add_parser('logs',
                                           help='server logs')
        parse_logs.add_argument('HOST',
                                default="localhost",
                                help='specify host to get logs from')
        parse_logs.set_defaults(func=logs.logs.main)

        # register
        parse_register = subparsers.add_parser('register',
                                               help='create an account')
        parse_register.add_argument('EMAIL',
                                    help='email address')
        parse_register.add_argument('USERNAME',
                                    help='username')
        parse_register.add_argument('PASSWORD',
                                    help='password')
        parse_register.set_defaults(func=register.register.main)

        # search
        parse_search = subparsers.add_parser('search',
                                            help='search for files')
        parse_search.set_defaults(func=search.search.main)
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
                                 default=socket.getfqdn(),
                                 help='specify host to run on')
        parse_start.add_argument('-P', '--port',
                                 type=int, default=3469,
                                 help='specify port to run on')
        if len(sys.argv) > 1:
            if sys.argv[1] == 'start':
                parse_start.set_defaults(func=start.start.main(self, parser.parse_args()))

        # stop
        parse_stop = subparsers.add_parser('stop',
                                           help='stop the ink service')
        parse_stop.set_defaults(func=stop.stop.main)

        # unwatch
        parse_unwatch = subparsers.add_parser('unwatch',
                                              help='stop watching a directory')
        parse_unwatch.add_argument('DIRECTORY',
                                   help='specify directory to stop watching')
        parse_unwatch.set_defaults(func=unwatch.unwatch.main)

        # version
        parse_version = subparsers.add_parser('version',
                                           help='show version')
        parse_version.set_defaults(func=version.version.main)

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
        if len(sys.argv) > 1:
            if sys.argv[1] == 'watch':
                parse_watch.set_defaults(func=watch.watch.main(self, parser.parse_args()))

        args = parser.parse_args()
        if args.func:
            args.func(args)

def main():
    cli().parse_args()

if __name__ == "__main__": # pragma: no cover
    main()

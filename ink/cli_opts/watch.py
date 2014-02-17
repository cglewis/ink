"""
This module is the watch command of ink.

Created on 16 February 2014
@author: Charlie Lewis
"""

import redis

class watch(object):
    """
    This class is responsible for the watch command of the cli.
    """
    @classmethod
    def main(self, parent, args):
        # !! TODO
        print args
        if args.recursive:
            print 1
        print args.DIRECTORY
        # check if this directory is already being watched
        # check if using the same parameters, update if different
        try:
            # !! TODO
            parent.r.set("foo",args.DIRECTORY)
        except Exception as e:
            print e
        # !! TODO
        # if the server is already started, index this newly added directory

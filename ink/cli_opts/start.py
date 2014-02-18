"""
This module is the start command of ink.

Created on 16 February 2014
@author: Charlie Lewis
"""

import os
import time

from stat import *

class start(object):
    """
    This class is responsible for the start command of the cli.
    """
    @classmethod
    def main(self, parent, args):
        # create a file for registration purposes
        # !! TODO

        # check if key for this host already exists
        # !! TODO

        # otherwise add a new key to the hosts list in redis
        parent.r.rpush('hosts', args.host)

        # get known directories
        # !! TODO
        directories = ["/"]
        for directory in directories:
            # index known directories for this host
            for dirname, dirnames, filenames in os.walk(directory):
                # print path to all filenames.
                for filename in filenames:
                    # add file to the host:dir list
                    parent.r.rpush(args.host+":"+directory, os.path.join(dirname, filename))
                    print os.path.join(dirname, filename)
                    try:
                        st = os.stat(os.path.join(dirname, filename))
                        print "\tfile size: ",st[ST_SIZE],
                        print "\tfile modified: ",time.asctime(time.localtime(st[ST_MTIME])),
                        print "\tfile last accessed: ",time.asctime(time.localtime(st[ST_ATIME])),
                        try:
                            import pwd # not available on all platforms
                            userinfo = pwd.getpwuid(st[ST_UID])
                        except (ImportError, KeyError):
                            print "failed to get the owner name for", file
                        else:
                            print "\tfile owned by:", userinfo[0]
                    except:
                        print "no metadata"

                # editing the 'dirnames' list will stop os.walk() from recursing into there.
                if '.git' in dirnames:
                    # don't go into any .git directories.
                    dirnames.remove('.git')

"""
This module is the start command of ink.

Created on 16 February 2014
@author: Charlie Lewis
"""

import os
import sys
import time

from stat import *

class start(object):
    """
    This class is responsible for the start command of the cli.
    """
    @classmethod
    def main(self, parent, args):
        omitted_dirs = ['/dev', '/proc', '/sys', '/Volumes', '/mnt', '/net']

        # create a file for registration purposes
        # !! TODO

        # check if key for this host already exists
        # !! TODO

        # otherwise add a new key to the hosts list in redis
        parent.r.rpush('hosts', args.host)

        # get known directories
        # !! TODO
        directories = ["/"]
        # !! TODO if directory starts with any of the omitted_dirs, remove from omitted_dirs
        for directory in directories:
            # index known directories for this host
            for dirname, dirnames, filenames in os.walk(directory):
                if dirname in omitted_dirs:
                    del dirnames[:]
                else:
                    # print path to all filenames.
                    for filename in filenames:
                        rows,columns = os.popen('stty size', 'r').read().split()
                        rows = int(rows)
                        columns = int(columns)

                        # add file to the host:dir list
                        parent.r.rpush(args.host+":"+directory, os.path.join(dirname, filename))
                        sys.stdout.write('\r')
                        sys.stdout.write(' ' * columns)
                        sys.stdout.write('\r')
                        sys.stdout.write('processing: {}'.format(os.path.join(dirname, filename)[:columns-13]))
                        sys.stdout.flush()
                        try:
                            st = os.stat(os.path.join(dirname, filename))
                            parent.r.hmset(args.host+":"+directory+":"+os.path.join(dirname, filename),
                                           "size", st[ST_SIZE],
                                           "modified", time.asctime(time.localtime(st[ST_MTIME])),
                                           "accessed", time.asctime(time.localtime(st[ST_ATIME])))
                            #print "\tfile size: ",st[ST_SIZE],
                            #print "\tfile modified: ",time.asctime(time.localtime(st[ST_MTIME])),
                            #print "\tfile last accessed: ",time.asctime(time.localtime(st[ST_ATIME])),
                            try:
                                import pwd # not available on all platforms
                                userinfo = pwd.getpwuid(st[ST_UID])
                            except (ImportError, KeyError):
                                junk = 1
                                #print "failed to get the owner name for", file
                            else:
                                parent.r.hset(args.host+":"+directory+":"+os.path.join(dirname, filename),
                                              "owner", userinfo[0])
                                #print "\tfile owned by:", userinfo[0]
                        except:
                            junk = 1
                            #print "no metadata"
                # editing the 'dirnames' list will stop os.walk() from recursing into there.
                if '.git' in dirnames:
                    # don't go into any .git directories.
                    dirnames.remove('.git')
        print

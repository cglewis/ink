"""
This module is the start command of ink.

Created on 16 February 2014
@author: Charlie Lewis
"""

import itertools
import json
import os
import socket
import sys
import time

from multiprocessing import Pool
from multiprocessing import cpu_count
from stat import *

def process_dirs(filename, parent):
    print filename, parent
    return

def func_star(a_b):
    return process_dirs(*a_b)

class start(object):
    """
    This class is responsible for the start command of the cli.
    """
    @classmethod
    def main(self, parent, args):
        pool_size = cpu_count()*2
        omitted_dirs = ['/dev', '/proc', '/sys', '/Volumes', '/mnt', '/net']
        ink_directory = "/var/lib/ink"
        host_file = os.path.join(ink_directory, 'host')
        ink_host = args.host

        # check if file for host already exists
        # if it exists, and host arg isn't default, update
        if os.path.isfile(host_file):
            if args.host != socket.getfqdn():
                with open(host_file, 'w') as f:
                    f.write(ink_host)
            else:
                with open(host_file, 'r') as f:
                    ink_host = f.readline()

        # create a file for host registration purposes
        if not os.path.exists(ink_directory):
            os.makedirs(ink_directory)
            with open(host_file, 'w') as f:
                f.write(ink_host)

        # check if key for this host already exists
        num_hosts = parent.r.llen('hosts')
        found = i = 0
        while i < int(num_hosts):
            if parent.r.lindex('hosts', i) == ink_host:
                found = 1
            i += 1

        # otherwise add a new key to the hosts list in redis
        if not found:
            parent.r.rpush('hosts', ink_host)

        # get known directories
        # !! TODO
        directories = ["/"]

        # !! TODO if directory starts with any of the omitted_dirs,
        #         remove from omitted_dirs
        pool = Pool(processes=pool_size)
        for directory in directories:
            # index known directories for this host
            for dirname, dirnames, filenames in os.walk(directory):
                if dirname in omitted_dirs:
                    del dirnames[:]
                else:
                    # print path to all filenames.
                    foo = 1
                    pool.map(func_star, itertools.izip(filenames, itertools.repeat(foo)))

                    #for filename in filenames:
                    #    rows,cols = os.popen('stty size', 'r').read().split()
                    #    rows = int(rows)
                    #    cols = int(cols)

                    #    # add file to the host:dir list
                    #    parent.r.rpush(args.host+":"+directory, os.path.join(dirname, filename))
                    #    sys.stdout.write('\r')
                    #    sys.stdout.write(' ' * cols)
                    #    sys.stdout.write('\r')
                    #    sys.stdout.write('processing: {}'.format(os.path.join(dirname, filename)[:cols-13]))
                    #    sys.stdout.flush()
                    #    try:
                    #        st = os.stat(os.path.join(dirname, filename))
                    #        value = json.dumps({"size": st[ST_SIZE],
                    #                            "modified": time.asctime(time.localtime(st[ST_MTIME])),
                    #                            "accessed": time.asctime(time.localtime(st[ST_ATIME]))})
                    #        # todo this should probably be under a list called 'host:directory:file'
                    #        parent.r.hmset(args.host+":"+directory+":"+os.path.join(dirname, filename),
                    #                       json.loads(value))
                    #        #print "\tfile size: ",st[ST_SIZE],
                    #        #print "\tfile modified: ",time.asctime(time.localtime(st[ST_MTIME])),
                    #        #print "\tfile last accessed: ",time.asctime(time.localtime(st[ST_ATIME])),
                    #        try:
                    #            import pwd # not available on all platforms
                    #            userinfo = pwd.getpwuid(st[ST_UID])
                    #            parent.r.hset(args.host+":"+directory+":"+os.path.join(dirname, filename),
                    #                          "owner", userinfo[0])
                    #            #print "\tfile owned by:", userinfo[0]
                    #        except (ImportError, KeyError):
                    #            junk = 1
                    #            #print "failed to get the owner name for", file
                    #    except:
                    #        junk = 1
                    #        #print "no metadata"
                # editing the 'dirnames' list will stop os.walk() from recursing into there.
                if '.git' in dirnames:
                    # don't go into any .git directories.
                    dirnames.remove('.git')
        print

#!/usr/bin/env python3.8

import argparse
import os.path
import datetime
import shutil
import sys

esi_dirs = """
tmp             root:root       1777
native          jetty:jetty     775
cache           root:root       775
tasks           jetty:jetty     775
lock            jetty:jetty     775
uploads         jetty:jetty     775"""

vpc_web_dirs = """
tmp             root:root       1777
sessions        jetty:jetty     775"""

parser = argparse.ArgumentParser(description="unpacks a WAR file to /mnt/ESI-YYYYMMDD")
parser.add_argument('war', nargs='?', type=str, default='/groups/dev/ESI.war',
                     help="location of WAR file to publish (default /groups/dev/ESI.war)")
parser.add_argument('-o', '--overwrite', action='store_true',
                     help="overwrite contents in existing directory")
parser.add_argument('-s', '--symlink', action="store_true", help="update the symlink automatically")
parser.add_argument('-q', '--quiet', action="store_true", help="unzip quietly")
args = parser.parse_args()

file = os.path.abspath(args.war)
warname = os.path.basename(file)
if warname.startswith('ESI'):
    warpath = 'ESI'
    mnt_dirs = esi_dirs
elif warname.startswith('vpc-web'):
    warpath = 'vpc-web'
    mnt_dirs = vpc_web_dirs
else:
    sys.exit("Unknown war.")


for dir_info in mnt_dirs.strip().split("\n"):
    info = dir_info.split()
    dir = "/".join(["/mnt", info[0]])
    usr_grp = info[1]
    if not os.path.exists(dir):
        os.makedirs(dir)
        os.system("chown %s %s" % (usr_grp, dir))
        try:
            perm = info[2]
            os.system("chmod %s %s" % (perm, dir))
        except IndexError:
            # No permission specified
            pass

currdir = os.getcwd()
now = datetime.date.today()
dr = '/mnt/%s-%i%02i%02i' % (warpath, now.year, now.month, now.day)
link_target = '/mnt/%s' % warpath
print(dr)
if os.path.exists(dr):
    print("target dir already exists!")
    if args.overwrite:
        print("removing it")
        shutil.rmtree(dr)
    else:
        sys.exit(1)
os.mkdir(dr)
os.chdir(dr)
os.system('unzip %s%s' % ('-q ' if args.quiet else '', file))
os.chdir(currdir)
os.system("chown -R jetty:jetty %s" % dr)
os.system("chmod -R g+rX %s" % dr)
if args.symlink:
    print("updating symlink")
    try:
        os.remove(link_target)
    except OSError:
        # symlink didn't exist
        pass
    os.symlink(dr, link_target)
else:
    print("Ready to swap the symlink: ")
    print("sudo ln -snf %s %s" % (dr, link_target))

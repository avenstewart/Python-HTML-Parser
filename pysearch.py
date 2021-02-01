#!/usr/bin/env python3
#from bs4 import BeautifulSoup as bs
import argparse
import sys
import os
import re


# filin = '/home/iykeln/Desktop/R_work/file1.html'
# webpage = urlopen(filin).read().decode('utf-8')
# soup = bs4.BeautifulSoup(webpage)


def finish():
    print("Exiting...")
    exit()


def delete_trailing_slash(path):
    if path[len(path) -1] == "/":
        path = path[0:len(path) -2]
    return path


def html_file_exists(path):
    try:
        xpath, xdirs, xfiles = next(os.walk(path))
    except:
        print("Reached end of directory tree.")

    for file in xfiles: # check to see if we are currently in the correct dir
        if file == "*.html":
            return True


def singlepatch(path):
    if html_file_exists(path):
        # CALL YOUR CUSTOM METHOD HERE
    else:
        print("No HTML files  found in provided path, exiting.")
        exit()


def bulkpatch(path):
    try:
        rpath, rdirs, rfiles = next(os.walk(path)) # top level directory
    except:
        print("Reached end of directory tree.")

    for dir in rdirs:
        if html_file_exists(rpath+"/"+dir):
            #CALL YOUR CUSTOM METHOD RECURSIVELY HERE
        else:
            x = 0
            try:
                path, dirs, files = next(os.walk(path+"/"+dir))
            except:
                print("Reached end of directory tree.")
            while x < 5: # maximum dir depth
                for dir in dirs:
                    if html_file_exists(dir):
                        patch_report(path+"/"+dir+"/report.html")
                    else:
                        path, dirs, files = next(os.walk(path+"/"+dir))
                        x += 1 # move into subdirectory
                break



def main(args):
    path = delete_trailing_slash(args.filepath)
    if args.single:
        singlepatch(path)
    else:
        bulkpatch(path)
    finish()


def _cli(args):
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    f_help = ("Provide the report directory '-f /path/to/file(s)")
    s_help = ("Search individual files.")
    b_help = ("Recursively search files in all subdirectories.")

    parser.add_argument('-f', '--filepath', help=f_help, required=True)
    parser.add_argument('-s', '--single', action="store_true", help=s_help)
    parser.add_argument('-b', '--bulk', action="store_true", help=b_help)

    args = parser.parse_args()

    if not (args.single or args.bulk):
        print("Insufficient arguments. -s or -b required")
        finish()

    return args


if __name__ == '__main__':
    main(_cli(sys.argv[1:]))

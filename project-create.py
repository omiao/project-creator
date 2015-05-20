#!/usr/bin/env python
# -*- utf-8 -*-

"""
This module is used to create project index file for cscope and ctags.
It can be used to filter files by their suffix and directory name.
User can also choose to create ctag file with the index file or not.
"""

import sys
import os
import fnmatch
import argparse


# Get the root path that used to index the project
rootpath = '.'
dirlists = []
includesuffix = []
excludesuffix = []
includedefault = False


def main():
    """TODO: Docstring for main.
    :returns: TODO

    """
    # Help mannul and argument function are created here:
    parser = argparse.ArgumentParser(prog='projcreate',
                                     description="""
    projcreate is a tool used to create project index file accroding
    with users' requirement.
    Users can specify which folder are included and not included and
    aslo what kind of files are included and what kinds of not included.""",
                                     epilog="""
    This tool is based on python 2.7
    bug report to (gmiao@sonicwall.com)
                                    """)

    # Now add all the command will be used for this tool
    parser.add_argument('-f', '--folder', nargs='*', help=""" List all the folders that needs to be included
                                                        in the project with + as prefix and folders that
                                                        will not included after it without any prefix
                                                    """, metavar='folders', dest=None)
    parser.add_argument('-t', '--type', nargs='*', help=""" List all file type that will be included in project
                                                    """, metavar='types', dest='insuffix')
    parser.add_argument('-e', '--extype', nargs='*', help=""" List all file type that will not be include in project
                                                    """, metavar='exclude types', dest='exsuffix')
    parser.add_argument('-a', '--all-others', nargs='?', help=""" For all other types of files which are not specified will
                                                    be included in the project
                                                    """, const=True, default=False, type=bool, metavar='include all other types', dest='includedefault')
    args = parser.parse_args()

    dirlist = []

    for folder in args.folder:
        if '+' in folder:
            if dirlist:
                dirlists.append(dirlist)
                dirlist = []
                dirlist.append(folder.strip('+'))
            else:
                rawdir = folder.strip('+')
                dirlist.append(rawdir)
        elif not dirlist:
            pass
        else:
            dirlist.append(folder)
    dirlists.append(dirlist)
    # print dirlists

    global includesuffix
    global excludesuffix
    global includedefault
    includesuffix = args.insuffix
    excludesuffix = args.exsuffix
    includedefault = args.includedefault


def filter_files(filename, filterlist):
    """TODO: Docstring for filter_files.

    :filename: TODO
    :filerlist: TODO
    :returns: TODO

    """
    for excludedir in filterlist:
        if excludedir in filename:
            return False
    return True


def filter_by_dirname(directory):
    """
    This function is used to filer directory by directory name
    either with prefix or not
    """
    for diritem in dirlists:
        includedir = diritem[0]
        if includedir in directory:
            # print "\nAdd Folder ", includedir
            excludedirs = diritem[1:]
            if excludedirs:
                # print "\nExclude files the following folders: ", excludedirs
                for excludedir in excludedirs:
                    if excludedir in directory:
                        return False
            return True


def filter_by_suffix(files):
    """
    This function is used to filter filename with a certain suffix which
    is not needed or only include file with certain suffix.
    1. If the file extension is in included suffix, then all the file with that
    extension should be included and others should be excluded.
    2. If the file extension is in the excluded suffix, then all the file with
    that extension should not be included and others should be included.
    """
    if includesuffix:
        for insuffix in includesuffix:
            extname = '*.' + insuffix
            if fnmatch.fnmatch(files, extname):
                return True

    if excludesuffix:
        for exsuffix in excludesuffix:
            extname = '*.' + exsuffix
            if fnmatch.fnmatch(files, extname):
                return False

    if includedefault:
        return True
    else:
        return False


def test():
    try:
        fp = open('cscope.files', 'w+')
        for dirlist in dirlists:
            if dirlist[0] != '.':
                path = rootpath + '/' + dirlist[0]
            else:
                path = rootpath
            filterlist = dirlist[1:]
            for dir, dirname, filename in os.walk(path):
                if filename:
                    for name in filename:
                        fullpath = dir + '/' + name
                        if filter_files(fullpath, filterlist) and filter_by_suffix(fullpath):
                            fp.write(fullpath + os.linesep)
                            # print fullpath
    except:
        print "Error"
        pass
    finally:
        fp.close()
        print "[+]cscope.files has been created......"
        print "[+]create cscope index......"
        os.system("cscope -Rbkq -i cscope.files")
        print "[+]create ctags......"
        os.system('ctags -L cscope.files --langmap=c++:+inl --langmap=c++:+txt --langmap=c++:+cfg --langmap=c++:+sym')

if __name__ == '__main__':
    main()
    test()


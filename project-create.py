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

# Help mannul and argument function are created here:
parser = argparse.ArgumentParser(prog='projcreate', 
								description=
								"""
projcreate is a tool used to create project index file accroding
with users' requirement. 
Users can specify which folder are included and not included and
aslo what kind of files are included and what kinds of not included.
								""", 
								epilog = 
								"""
This tool is based on python 2.7
bug report to (gmiao@sonicwall.com)
								""")#, formatter_class=argparse.RawDescriptionHelpFormatter)

# Now add all the command will be used for this tool
parser.add_argument('-f', '--folder', nargs='*', help=
												""" List all the folders that needs to be included
													in the project with + as prefix and folders that 
													will not included after it without any prefix
												""", metavar = 'folders', dest=None)
parser.add_argument('-t', '--type', nargs='*', help=
												""" List all file type that will be included in project 
												""", metavar = 'types', dest='includesuffix')
parser.add_argument('-e', '--extype', nargs='*', help=
												""" List all file type that will not be include in project 
												""", metavar = 'exclude types', dest='excludesuffix')
parser.add_argument('-a', '--all-others', nargs = '?', help=
												""" For all other types of files which are not specified will
												be included in the project
												""", const = True, default = False, type = bool, metavar = 'include all other types', dest='includedefault')
args = parser.parse_args()
print args.folder, args.includesuffix, args.excludesuffix

filedirs = []
tupledirs = ()
for dir in args.folder:
	if '+' in dir:
		rawdir = dir.strip('+')
		tupledirs = (rawdir)
		print rawdir
	else:
		pass

# Get the root path that used to index the project
rootpath = '.'

# Get directory names that used to filer the index file
filedir = [('firmware/fw', 'firmware/fw/resource'),
			('firmware/fw/resource/UI5/default/eng', ''),
			('firmware/gst/gstDictionary.c', ''),
			('firmware/h', ''),
			('firmware/bcp', ''),
			('firmware/libsrc/ip_net2-6.6', '')
		]

includesuffix = ['txt', 'c']
excludesuffix = ['png', 'gif']

includedefault = False
# Get directory names that used to index files
# includedir = [
		# 'firmware/fw/resource/UI5/default/eng/',
		# 'firmware/libsrc/ip_net2-6.6/'
		# ]

def filter_by_dirname(dir):
	"""
	This function is used to filer directory by directory name
	either with prefix or not
	"""
	for includedir, excludedir in filedir:
		if includedir in dir and (not excludedir or excludedir not in dir):
			return True
			
def filter_by_suffix(filename):
	"""
	This function is used to filter filename with a certain suffix which
	is not needed or only include file with certain suffix.
	1. If the file extension is in included suffix, then all the file with that
	extension should be included and others should be excluded.
	2. If the file extension is in the excluded suffix, then all the file with 
	that extension should not be included and others should be included.
	"""
	for insuffix in includesuffix:
		extname = '*.' + insuffix
		if fnmatch.fnmatch(filename, extname):
			return True
	for exsuffix in excludesuffix:
		extname = '*.' + exsuffix
		if fnmatch.fnmatch(filename, extname):
			# print '#' + filename
			return False 
	
	if includedefault:
		return True
	else:
		return False

def test():
	try:
		fp = open('cscope.files', 'w+')
		for dir, dirname, filename in os.walk(rootpath):
			if filter_by_dirname(dir):
				for name in filename:
					if name and filter_by_suffix(name):
						fp.write(dir + '/' + name + os.linesep)
						#print dir
	except:
		pass
	finally:
		fp.close()
		print "cscope.files has been created......"

if __name__ == '__main__':
	test()

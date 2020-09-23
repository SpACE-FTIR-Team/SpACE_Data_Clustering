#
# File and folder operations for SpACE
#
# Currently includes: selecting files in folder
# and subfolders, filtering files by filename
#
# TODO: file saving functions likely will go here

import os.path
import glob

def path_exists(folder):
	"""Just checks to see if a path is a valid path."""
	return os.path.exists(folder)

def collect_all_filenames(folder):
	"""Finds all files in a given folder and all of its
	subfolders. Returns a Python list where each entry
	is a filename with full path to the file."""
	return glob.glob(folder + '/**', recursive = True)


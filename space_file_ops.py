#
# File and folder operations for SpACE
#
# Currently includes: selecting files in folder
# and subfolders, filtering files by filename
#
# TODO: file saving functions likely will go here

import os.path

def path_exists(folder):
	return os.path.exists(folder)


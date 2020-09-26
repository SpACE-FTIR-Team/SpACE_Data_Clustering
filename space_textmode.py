#
# Text mode for SpACE for testing and development
#

import space_file_ops as fileops
import space_data_ops as dataops

def one_dobj(folder):
    """Get one data object.
    Accepts a path to the data files. Parses the first file found in that path
    that matches the filespec (tir, nicolet, specturm, .txt).
    Returns one data object."""
    filtered_file_list = get_file_list(folder)
    if filtered_file_list == None:
        return None
    print("Using first file found: %s" % filtered_file_list[0])
    # parse
    df = dataops.file_to_data_object(filtered_file_list[0:1])
    print("Parsed into %s data objects" % len(df))
    return df[0]

def all_dobj(folder):
    """Get all data objects.
    Accepts a path to the data files. Parses all the files found in that path
    that match the filespec (tir, nicolet, specturm, .txt).
    Returns a list of pandas dataframes."""
    filtered_file_list = get_file_list(folder)
    if filtered_file_list == None:
        return None
    # parse
    df = dataops.file_to_data_object(filtered_file_list)
    print("Parsed into %s data objects" % len(df))
    return df

def get_file_list(folder):
    # verify we have a good path
    if not fileops.path_exists(folder):
        # this is a fatal error - log to console
        print("Invalid path: %s" % folder)
        return None
    # search for all files in input folder and subfolders
    file_list = fileops.collect_all_filenames(folder)
    print("Found %s files and folders in %s" % (len(file_list), folder))
    # filter by filename
    filtered_file_list = fileops.filter_filenames(file_list)
    print("Found %s files matching the filename filter criteria" % len(filtered_file_list))
    return filtered_file_list

def simulate_go(folder):
    """Run the same basic steps that the GUI go button would do."""
    data_objects = all_dobj(folder)
    dataops.reindex(data_objects)
    return data_objects
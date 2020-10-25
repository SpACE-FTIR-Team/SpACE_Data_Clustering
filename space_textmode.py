#
# Text mode for SpACE for testing and development
#

import space_file_ops as fileops
import space_data_ops as dataops
import DataObject

all_dobjs = []
reindexed_dobjs = []
truncated_dobjs = []
aligned_dobjs = []
normalized_dobjs = []

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

def get_all_dobj(folder):
    """Get all data objects.
    Accepts a path to the data files. Parses all the files found in that path
    that match the filespec (tir, nicolet, specturm, .txt).
    Returns a list of pandas dataframes."""
    filtered_file_list = get_file_list(folder)
    if filtered_file_list == None:
        return None
    # parse
    print("Parsing...")
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

def copy_dobjs(data_objects_list):
    copied = []
    for d_o in data_objects_list:
        desc = d_o.descriptive
        prs  = d_o.pairs
        fn = d_o.filename
        new_dobj = DataObject.DataObject(desc, prs, fn)
        copied.append(new_dobj)
    return copied

def simulate_go(folder):
    """Run the same basic steps that the GUI go button would do."""

    global all_dobjs, reindexed_dobjs, truncated_dobjs, aligned_dobjs, normalized_dobjs

    data_objects = get_all_dobj(folder)

    print("Re-indexing...")
    dataops.reindex(data_objects)
    reindexed_dobjs = copy_dobjs(data_objects)
    print("** <module>.reindexed_dobjs now contains re-indexed data objects")

    print("Calculating common range...")
    min, max = dataops.find_common_range(data_objects)
    if (min, max) == (None, None):
        print("No range in common!")
        return None
    else:
        print("Common wavelength range is %s to %s" % (min, max))

    print("Truncating data to range %s to %s..." % (min, max))
    dataops.truncate(data_objects, min, max)
    truncated_dobjs = copy_dobjs(data_objects)
    print("** <module>.truncated_dobjs now contains truncated data objects")

    print("Finding highest resolution file...")
    max_res_index = dataops.find_max_res(data_objects)
    print("Aligning the data...")
    dataops.align(data_objects, max_res_index)
    aligned_dobjs = copy_dobjs(data_objects)
    print("** <module>.aligned_dobjs now contains aligned data objects")

    print('Normalizing data...')
    data_objects = dataops.linear_normalize(data_objects)
    normalized_dobjs = copy_dobjs(data_objects)
    print("** <module>.normalized_dobjs now contains normalized data objects")

    print("Combining...")
    dataset = dataops.combine(data_objects)

    return dataset
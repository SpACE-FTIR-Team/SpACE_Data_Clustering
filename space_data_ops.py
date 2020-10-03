#
# Data functions for SpACE
# 
# Currently includes: import NASA ECOstress Spectral Library files
# into DataObjects (see DataObject.py), re-index dataframes,
# find common range, truncate dataframes to common range,
# align data to be in the same step, and add in missing values 
# with interpolation
#
# TODO: normalization, PCA?

import pandas as pd
from DataObject import DataObject

# columns include overflow for extra ":" characters found in the description field
columns = ['descriptor', 'value', 'overflow', 'overflow2', 'overflow3']

# Function: File to DataObject
# Description: This function takes a list of files (files variable above) and converts them to two pandas
# DataFrames, one of descriptive data, and one of float values for the xy_pairs. The DataFrames are used as
# parameters to construct a DataObject. The function then returns an array of each file as a DataObject.
#
# Returns: DataObjects
#
def file_to_data_object(file_list):
    DataObjects = []
    # DataFrame conversion - one DF for descriptive data, and one DF for the (x, y) pairs
    for item in file_list:
        data = pd.read_csv(item, sep=":", header=None, engine="python", names=columns, quotechar='"')

        pairs, pair_index, desc_index = [], 0, 0
        # the first column contains both the pairs and the labels for descriptive data
        first_col = data['descriptor']
        # search every row in the first column for \t
        for value in first_col:
            # find the index where xy_pairs begin
            # I noticed that all the pairs contain tabs, so search each file for the first occurrence of \t
            if "\t" in value:
                pairs.append(value.split("\t"))
                if pair_index == 0:
                    pair_index = first_col[first_col == value].index[0]
            # find the index for the description field for description processing below
            elif "Description" in value:
                desc_index = first_col[first_col == "Description"].index[0]

        # convert pairs to DataFrame, with column labels for given X Units and Y Units
        if pair_index != 0:
            descriptive_data = data.head(pair_index)
            xy_pairs = pd.DataFrame(pairs,
                                    columns=[descriptive_data.loc[14, 'value'],
                                             descriptive_data.loc[15, 'value']])
        # throw an error if the pair_index is zero (means that "\t" was not found in the file)
        else:
            descriptive_data = data
            raise Exception(f"Numerical coordinate pairs could not found for {item}")

        # Description Processing: for DataFrame conversion, overflow columns were needed
        # for the descriptions of each spectra, the code below removes the overflow.
        # description = descriptive_data.loc[10, 'overflow, overflow2, or overflow3']

        # Make a copy, this is recommended by pandas documentation for modifying individual cells
        descriptive_copy = descriptive_data.copy()
        # if overflow is nan, drop overflow columns
        if pd.isna(descriptive_data.loc[desc_index, 'overflow']):
            descriptive_data = descriptive_data.dropna(axis=1)

        # if overflow2 is nan, combine value and overflow for description, and drop overflow columns
        elif pd.isna(descriptive_data.loc[desc_index, 'overflow2']):
            combine_string = ': ' + descriptive_data.loc[desc_index, 'overflow']
            descriptive_copy.loc[desc_index, 'value'] = descriptive_data.loc[desc_index, 'value'] + combine_string
            descriptive_data = descriptive_copy.drop(['overflow', 'overflow2', 'overflow3'], axis=1)

        # if overflow3 is nan, combine value and overflow1 and 2 for description, and drop overflow columns
        elif pd.isna(descriptive_data.loc[desc_index, 'overflow3']):
            combine_string = ': ' + descriptive_data.loc[desc_index, 'overflow'] + ': ' + \
                             descriptive_data.loc[desc_index, 'overflow2']
            descriptive_copy.loc[desc_index, 'value'] = descriptive_data.loc[desc_index, 'value'] + combine_string
            descriptive_data = descriptive_copy.drop(['overflow', 'overflow2', 'overflow3'], axis=1)

        # else combine all overflow columns with value, and drop overflow columns
        else:
            combine_string = ': ' + descriptive_data.loc[desc_index, 'overflow'] + ': ' + \
                             descriptive_data.loc[desc_index, 'overflow2'] + ': ' + \
                             descriptive_data.loc[desc_index, 'overflow3']
            descriptive_copy.loc[desc_index, 'value'] = descriptive_data.loc[desc_index, 'value'] + combine_string
            descriptive_data = descriptive_copy.drop(['overflow', 'overflow2', 'overflow3'], axis=1)

        # DataFrame values are initially typed as objects, code below is conversion to workable data types
        # convert descriptive data to strings
        descriptive_data = descriptive_data.convert_dtypes(convert_string=True)
        # convert xy_pairs to floats
        xy_pairs[xy_pairs.columns[0]] = xy_pairs[xy_pairs.columns[0]].astype(float)
        xy_pairs[xy_pairs.columns[1]] = xy_pairs[xy_pairs.columns[1]].astype(float)
        # construct DataObject with DataFrames and filepath (may want more parameters later)
        processed_item = DataObject(descriptive_data, xy_pairs, item)
        DataObjects.append(processed_item)

    return DataObjects

def reindex(data_objects):
    """This function takes a list of data objects, iterates over them,
    and changes the index in the 'pairs' dataframe of each data object.
    The integer index [0, 1, 2, ..., n] is dropped.
    The ' Wavelength (micrometers)' [note the leading space] column becomes
    the new index. [note also some columns have (micrometer) without
    the plural s]
    The ' Wavelength (micrometers)' column is renamed 'wavelength'.
    Dataframes are modified in-place, so None is returned."""
    for dobj in data_objects:
        dataframe = dobj.pairs
        wavelength_col_name = dataframe.columns[0]
        dataframe.rename(columns={wavelength_col_name: 'wavelength'}, inplace=True)
        dataframe.set_index('wavelength', inplace=True)
        dataframe.sort_index(inplace = True)
    return None

def find_common_range(data_objects):
    """This function takes a list of data objects, iterates over them,
    and checks the minimum and maximum wavelength in every 'pairs' dataframe,
    keeping track of the highest minimum and lowest maximum seen.
    When done, if min < max, then the common range of all data objects is
    min to max. Return (min, max).
    If min > max, the data objects have no range in common. Return (None, None)."""
    highest_minimum = data_objects[0].pairs.index.min()
    lowest_maximum = data_objects[0].pairs.index.max()
    for dobj in data_objects[1:]:
        dataframe = dobj.pairs
        if dataframe.index.min() > highest_minimum:
            highest_minimum = dataframe.index.min()
        if dataframe.index.max() < lowest_maximum:
            lowest_maximum = dataframe.index.max()
    if highest_minimum < lowest_maximum:
        return highest_minimum, lowest_maximum
    else:
        return None, None

def truncate(data_objects, min, max):
    """This function takes a list of data objects, iterates over them,
    and truncates every 'pairs' dataframe to remove any rows (wavelengths)
    below 'min' and above 'max'. The result is that all 'pairs' dataframes
    will have the same range of wavelengths. (Note that wavelengths are
    not aligned here; that comes later.)
    Pandas can't truncate in place, so a new truncated dataframe is
    constructed and then the DataObject 'pairs' dataframe is replaced
    with the new dataframe. Returns None."""
    for dobj in data_objects:
        original_dataframe = dobj.pairs
        truncated_dataframe = original_dataframe.truncate(before=min, after=max, axis='index', copy = True)
        dobj.pairs = truncated_dataframe
    return None

def find_max_res(data_objects):
    """This function takes a list of data objects and the range common to them, iterates over them, and finds the
    object with the most points.  It will return the index of this object"""
    max_pts = 0
    max_pts_index = 0
    for i in range(len(data_objects)):
        cur_pts = data_objects[i].pairs.size
        if cur_pts > max_pts:
            max_pts = cur_pts
            max_pts_index = i
    return max_pts_index


def align(data_objects, align_to):
    """This function takes a list of data objects, iterates over them, and makes every 'pairs' dataframe use the same
    x axis.  The result is that all 'pairs' dataframes will use the same x axis and thus be aligned.  This will then fill in 
    any missing values caused by the alignment using.  align_to should also be the index of the data object to align to
    and contains the x axis that all dataobjs should be aligned to."""

    alignment_pairs = data_objects[align_to].pairs
    for dobj in data_objects:
        ( _ ,dobj.pairs) = alignment_pairs.align(dobj.pairs, join="outer", axis = 0)
        dobj.pairs = dobj.pairs.interpolate()
        ( _ , dobj.pairs) = alignment_pairs.align(dobj.pairs, join ="left", axis = 0)
    return None

def combine(data_objects):
    """This function takes a list of data objects all sharing a common x coordinate and outputs them all as one block
    This block will have each data_object taking up one row where each column is a different y coordinate.
    Returns a block of data"""
    data_block = pd.concat([dobj.pairs.transpose() for dobj in data_objects], ignore_index = True)
    return data_block
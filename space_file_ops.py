# -*- coding: utf-8 -*-
# 
# Spectral Analysis Clustering Explorer (SpACE)
# Missouri State University
# CSC450 Fall 2020 - Dr. Razib Iqbal
#
# Team 2 (FTIR/ECOSTRESS/SpACE team):
# Austin Alvidrez
# Brad Meyer
# Collin Tinen
# Kegan Moore
# Sam Nack
#
# Copyright 2020 Austin Alvidrez, Brad Meyer, Collin Tinen,
# Kegan Moore, Sam Nack
#
# Spectral Analysis Clustering Explorer (SpACE) is free software:
# you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Spectral Analysis Clustering Explorer (SpACE) is distributed in
# the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with Spectral Analysis Clustering Explorer (SpACE).
# If not, see <https://www.gnu.org/licenses/>.

# space_file_ops.py
# This file contains functions that interact with files and folders.
#
# Includes: check if a path is valid, selecting files in
# a folder and subfolders, filtering files by filename, save modified
# data files as .csv, save data blocks as .csv, save cluster
# compositions as .csv

import os.path
import glob


def path_exists(folder):
    """
    Checks to see if a path exists.
    Returns True if it exists.
    """
    return os.path.exists(folder)


def collect_all_filenames(folder):
    """
    Finds all files in a given folder and all of its
    subfolders. Returns a Python list where each entry
    is a filename with full path to the file.
    """
    return glob.glob(folder + '/**', recursive=True)


def filter_filenames(file_list):
    """
    Iterates through a list of files and retains only
    those that have 'tir' 'nicolet' 'spectrum' and '.txt'
    in the filename. Returns a Python list.
    """
    return list(filter(lambda filename: 'tir' in filename
                                        and 'nicolet' in filename
                                        and 'spectrum' in filename
                                        and '.txt' in filename,
                       file_list))


def save_data_files(folder, suffix, data_objects):
    """
    Accepts a specified filepath, a suffix to add to it,
    and a list of data_objects. Iterates through them all
    and saves them to the filepath with the suffix added on.
    Saves as .csv
    """
    dir_name = os.path.join(folder, suffix)
    if not path_exists(dir_name):
        os.mkdir(dir_name)
    for dobj in data_objects:
        file_name = dobj.filename.rstrip("txt") + "csv"
        save_string = os.path.join(dir_name, file_name)
        dobj.pairs.to_csv(save_string)  # other arguments can be supplied, check pandas docs


def save_block_data(folder, suffix, dataset):
    """
    Accepts a specified filepath, a suffix to add to it,
    and a single combined dataframe.
    Saves as .csv
    """
    # suffix might be a single string in the case of saving
    # the combined data block, or it might be a tuple containing
    # multiple strings (nested subfolder names) in the case
    # of saving PCA data
    if isinstance(suffix, tuple):
        dir_name = os.path.join(folder, *suffix)
    else:
        dir_name = os.path.join(folder, suffix)
    if not path_exists(dir_name):
        os.mkdir(dir_name)
    save_string = os.path.join(dir_name, "data_block.csv")
    dataset.to_csv(save_string)  # other arguments can be supplied, check pandas docs


def save_composition(folder, clustering_type, file_suffix, c):
    """
    Accepts a specified filepath, a clustering type,
    a filename suffix, and a cluster composition dataframe.
    Saves the cluster composition info.
    """
    if not path_exists(folder):
        os.mkdir(folder)
    file_name = clustering_type + "_composition_" + file_suffix + ".csv"
    save_string = os.path.join(folder, file_name)
    c.to_csv(save_string)  # other arguments can be supplied, check pandas docs

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

# DataObject.py
# This is a class definition for the data object.
#
# Each input file is represented as one data object.
# descriptive_data and xy_pairs are pandas DataFrames
# filepath is the filepath in form ("ecostress_data_files\\datafile.txt")

class DataObject:
    def __init__(self, descriptive_data, xy_pairs, filepath):
        self.descriptive = descriptive_data
        self.pairs = xy_pairs
        self.path = filepath
        self.filename = self.path.split("\\")[-1]

    def __str__(self):
        return self.path

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

# space_main.py
# This is the main entry point for the SpACE application, GUI version.
#
# Configuration options and defaults are specified here.
# Then the GUI is launched.

from os import getcwd
import space_gui as gui

# linked to functional requirement #13 - pre-populating default values for kmeans and DBSCAN clustering algorithms
CONFIG = {
    "APP_NAME": "SpACE",
    "APP_VERSION": "1.0.0",
    "PCA_BY_DEFAULT": True,
    "DEFAULT_PCA_DIMENSIONS": 8,
    "SAVE_AFTER_DATA_MODIFICATION_BY_DEFAULT": False,
    "DEFAULT_KMEANS_K": 8,
    "DEFAULT_DBSCAN_EPS": 1.0,
    "DEFAULT_DBSCAN_MINPTS": 3,
    "DEFAULT_INPUT_PATH": None,
    "KMEANS_SAVING": {"save": True,
                      "by_type": True,
                      "by_class": True,
                      "by_subclass": True},
    "DBSCAN_SAVING": {"save": True,
                      "by_type": True,
                      "by_class": True,
                      "by_subclass": True},
}


def main():
    # add current directory to the config -- used for initial input folder path
    CONFIG["DEFAULT_INPUT_PATH"] = getcwd()
    gui.launch_gui(CONFIG)


if __name__ == '__main__':
    main()

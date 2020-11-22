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
# License:

# space_main.py
# This is the main entry point for the SpACE application, GUI version.
#
# Configuration options and defaults are specified here.
# Then the GUI is launched.

from os import getcwd
import space_gui as gui

CONFIG = {
    "APP_NAME": "SpACE",
    "APP_VERSION": "0.9.0",
    "PCA_BY_DEFAULT": True,
    "DEFAULT_PCA_DIMENSIONS": 2,
    "SAVE_AFTER_DATA_MODIFICATION_BY_DEFAULT": False,
    "DEFAULT_KMEANS_K": 8,
    "DEFAULT_DBSCAN_EPS": 1.0,
    "DEFAULT_DBSCAN_MINPTS": 3,
    "DEFAULT_INPUT_PATH": None,
    "KMEANS_SAVING": {  "save": True,
                        "by_type": True,
                        "by_class": True,
                        "by_subclass": True},
    "DBSCAN_SAVING": {  "save": True,
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

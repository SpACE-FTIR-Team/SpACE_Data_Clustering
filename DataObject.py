#
# This class is a container object for each data file.
# descriptive_data and xy_pairs are pandas DataFrames
# filepath is the filepath in form ("ecostress_data_files\\datafile.txt")
#

class DataObject:
    def __init__(self, descriptive_data, xy_pairs, filepath):
        self.descriptive = descriptive_data
        self.pairs = xy_pairs
        self.path = filepath
        # self.filename = self.path.split("\\")[1]

    def __str__(self):
        return self.path

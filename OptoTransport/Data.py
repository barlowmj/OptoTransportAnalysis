from tkinter import filedialog as fd
import os
import warnings
import sqlalchemy
import json
import pandas
import numpy
from collections import OrderedDict

class Data:

    # General data class. Reads data from database file and converts to pandas 
    # dataframe to be passed on to TransportData and OpticsData. Allows for 
    # many different types of data file conversions.

    def __init__(self, filename="", filename_md=""):
        # check if file given; if not, ask for user to select a file 
        # (starts looking from my personal folder in Dropbox)
        if not filename=="":
            self.filename = filename
        else:
            self.filename = fd.askopenfilename(title="Please select the database file:",
                             initialdir='/Users/jackbarlow/Dropbox/Jack B/data')
        
        self.dir = os.path.dirname(self.filename)
        split_filename = os.path.splitext(self.filename)
        self.file_ext = split_filename[1]

        # if filename_md is specified, then assigns it to self.filename_md
        # if filename_md not specified, checks if corresponding json file 
        # exists, otherwise asks for user input
        if not filename_md == "":
            self.filename_md = filename_md
        else:
            if os.path.exists(split_filename[0] + '.json') and os.path.getsize(split_filename[0] + '.json') > 0:
                self.filename_md = split_filename[0] + '.json'
            else:
                self.filename_md = fd.askopenfilename(title='Please select corresponding metadata file:', 
                                    initialdir=self.dir)

        # initialize data structure with pandas
        self.data = initData(self.file_ext, self.filename)
        
        # if no metadata file given, raise warning; otherwise, try to 
        # initialize metadata structure with pandas
        if self.filename_md == "":
            warnings.warn('No metadata file selected')
            self.metadata = {}
        else:
            split_filename_md = os.path.splitext(self.filename_md)
            self.file_ext_md = split_filename_md[1]
            self.metadata = initMetadata(self.file_ext_md, self.filename_md)
        
# Helper functions ------------------------------------------------------------

# initializers

def initData(file_ext, filename):

    # Initializes data from file using list of supported file types

    supported_file_types = ['.db', '.csv']
    assert(file_ext in supported_file_types), 'Data file type not supported'

    if file_ext == '.db':
        return initDataFromDB(filename)
    elif file_ext == '.csv':
        return initDataFromCSV(filename)
    else:
        warnings.warn('Unexpected potential error')
        return

def initMetadata(file_ext_md, filename_md):

    # Initializes metadata from file using list of supported file 
    # types. Also allows initialization if no metadata file given.

    supported_file_types_md = ['.json']
    assert(file_ext_md in supported_file_types_md), 'Metadata file type not supported'
    
    if file_ext_md == '.json':
        return initMetadataFromJSON(filename_md)
    else:
        warnings.warn('Unexpected potential error')
        return

# initializers for specific file formats

def initDataFromDB(filename):
    # initialize connection to database
    eng = sqlalchemy.create_engine(f'sqlite:///{filename}')
    data = OrderedDict()
    data["experiments"] = pandas.read_sql('experiments', eng.connect())
    data["runs"] = pandas.read_sql('runs', eng.connect())

    # eventually should try to correlate runs to corresponding experiment id? or something like that
    for ind, row in data["runs"].iterrows():
        run_params = row["parameters"].split(',')
        data[f'{row["result_table_name"]}'] = pandas.read_sql(f'{row["result_table_name"]}', 
                                                eng.connect()).groupby(run_params[0]).agg(numpy.nanmean)
    return data

def initDataFromCSV(filename):
    data = pandas.read_csv(filename)
    return data

def initMetadataFromJSON(filename_md):
    if filename_md == '':
        metadata = float("NaN")
        warnings.warn('No metadata file to read')
    else:   # need to update to catch file exception errors
        with open(filename_md, "r") as file:
            metadata = json.load(file)
    return metadata

# helpful function which allows you to make a json file from a dict if you 
# don't have associated metadata already recorded

def createMetadataIfNone(dict_to_write):
    filename = fd.askopenfilename(title="Please select the file you wish to create an associated metadata file for:", 
                                  initialdir='/Users/jackbarlow/Dropbox/Jack B/data')
    dir = os.path.dirname(filename)
    filename_json = os.path.splitext(filename)[0] + '.json'
    with open(filename_json, "w") as file:
        json.dump(dict_to_write, file)



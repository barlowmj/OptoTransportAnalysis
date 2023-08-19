from tkinter import filedialog as fd
import os
import warnings
import sqlalchemy
import json
import pandas
import numpy
from collections import OrderedDict

class Data:
    """
    Abstract class which containing data and metadata dict for easy analysis.

    Reads data from source file and converts to pandas DataFrame, then 
    reads some associated file containing metadata to put in a dict. 
    Passes these attributes down to TransportData and OpticsData child 
    classes for more specific operations.

    Attributes
    ----------
    data : pandas Dataframe 
        pandas Dataframe containing experimental data read in from one 
        of supported filetypes.

    metadata : Dict, optional
        dict containing information about an experiment (e.g., amplifier 
        gain, excitation wavelength, etc.) read in from one of 
        supported filetypes.

    filename, filename_md : path or path-like str
        A reference to the file used to initialize the data or metadata 
        attributes (if given).
    
    Methods
    -------

    __init__(filename=None, filename_md=None, init_dir="")
        Constructor. All parameters optional, but will not run if no 
        file selected for data. filename describes the relevant data file, 
        filename_md the relevant metadata file, and init_dir gives the
        initial folder from which to search for a data file if searching
        manually via tkinter.fieldialog GUI.

    __initData()
        Initializes data using one of separate methods on supported
        file types. Currently supported file types include: .db, .csv
        .db requires specific database formatting from QCoDeS-acquired
        data.

    __initMetadata()
        Initializes metadata using one of separate methods on supported
        file types. Currently supported file types include: .json

    __initDataFromDB()
        Initializes data from .db files formatted by QCoDeS.

    __initDataFromCSV()
        Initializes data from .csv files using pandas.to_csv().

    __initMetadataFromJSON()
        Initializes metadata from .json files using json.write().

    """

    #### Constructor ---------------------------------------------------------

    def __init__(self, filename=None, filename_md=None, init_dir=""):
        """
        Constructor for Data class. 
        
        By default, asks user to select a file using a tkinter.filedialog GUI 
        and tries to initialize a Data object from that file. Can also 
        provide a filename directly as input, or provide a directory 
        from which to begin the search via the GUI.

        Parameters
        ----------

        filename, filename_md : path or path-like str, default = None
            Reference to a file used to initialize filename or filename_md
            attribute of Data class.

        init_dir : path or path-like str, default = ""
            Reference to a file from which user can begin searching for 
            desired file through tkinter.filedialog GUI.

        Returns
        -------

        N/A

        """
        # Check if file given, otherwise prompt user to select file
        if not filename==None:
            self.filename = filename
        else:
            prompt_str = "Please select data file: "
            self.filename = fd.askopenfilename(title=prompt_str,
                                               initialdir=init_dir)

        # Assert that 
        assert(self.filename != None), "File not selected"
        
        dir = os.path.dirname(self.filename)
        split_filename = os.path.splitext(self.filename)

        # Check if file given, otherwise
        # -- Check if metadata file with similar name exists
        # -- If not, prompt user to select file
        if not filename_md == None:
            self.filename_md = filename_md
        else:
            if (os.path.exists(split_filename[0] + '.json') 
                and os.path.getsize(split_filename[0] + '.json') > 0):
                self.filename_md = split_filename[0] + '.json'
            else:
                prompt_str_md = "Please select metadata file: "
                self.filename_md = fd.askopenfilename(title=prompt_str_md, 
                                                      initialdir=dir)

        # Initialize self.data, notify of successful loading
        self.__initData()
        print(f'Successfully loaded data from {self.filename}')
        
        # Raise warning if no metadata discovered at this point, create empty dict if so
        # Otherwise, initialize self.metadata, notify of successful loading
        if self.filename_md == None:
            warnings.warn('No metadata file selected')
            self.metadata = {}
        else:
            self.__initMetadata()
        print(f'Successfully loaded metadata from {self.filename_md}')


    #### Methods -------------------------------------------------------------


    def __initData(self):
        """
        Initializes data from file from list of supported data types.
        """
        split_filename = os.path.splitext(self.filename)
        file_ext = split_filename[1]

        supported_file_types = ['.db', '.csv']
        assert(file_ext in supported_file_types), 'Data file type not supported'

        if file_ext == '.db':
            self.__initDataFromDB()
        elif file_ext == '.csv':
            self.__initDataFromCSV()
        else:
            warnings.warn('Unexpected potential error')
        return


    def __initMetadata(self):
        """
        Initializes metadata from file using list of supported file types. 
        """
        split_filename = os.path.splitext(self.filename_md)
        file_ext_md = split_filename[1]

        supported_file_types_md = ['.json']
        assert(file_ext_md in supported_file_types_md), 'Metadata file type not supported'
        
        if file_ext_md == '.json':
            self.__initMetadataFromJSON()
            return
        else:
            warnings.warn('Unexpected potential error')
            return

    ###### Initialization methods for specific file formats

    def __initDataFromDB(self):
        """
        Initializes data attribute from SQLite .db files using SQAlchemy

        This is a common format used by QCoDeS measurements. Formatted 
        specifically for .db files from  QCoDeS acquisition.
        """
        # Initialize connection to database with SQAlchemy, read experiments & runs
        eng = sqlalchemy.create_engine(f'sqlite:///{self.filename}')
        self.data = OrderedDict() 
        self.data["experiments"] = pandas.read_sql('experiments', eng.connect())
        self.data["runs"] = pandas.read_sql('runs', eng.connect())

        # eventually should try to correlate runs to corresponding experiment id? or something like that
        for ind, row in self.data["runs"].iterrows():
            run_params = row["parameters"].split(',')
            self.data[f'{row["result_table_name"]}'] = pandas.read_sql(f'{row["result_table_name"]}', 
                                                    eng.connect()).groupby(run_params[0]).agg(numpy.nanmean)
        return


    def __initDataFromCSV(self):
        """
        Initializes data attribute from .csv files by using the pandas.load_csv function
        """
        self.data = pandas.read_csv(self.filename)
        return


    def __initMetadataFromJSON(self):
        """
        Initializes metadata attribute from .json files using json.load function
        """
        with open(self.filename_md, "r") as file:
            self.metadata = json.load(file)
        return
            




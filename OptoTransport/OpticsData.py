import pandas
import os
import matplotlib.pyplot as plt
from Data import Data

class OpticsData(Data):
    # Base class for all transport data types. Initializes with connection to a 
    # database file containing sweep data and a metadata file containing instrument 
    # parameters for child classes to use.
    def __init__(self, fn="", fn_md=""):
        super().__init__(filename=fn, filename_md=fn_md)
        return
    
def average_signal(dat):
    assert type(dat) == OpticsData, "Input must be an OpticsData object"
    avg = dat.data.iloc[:,0:-1].sum() / dat.metadata['num_frames']
    return avg

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
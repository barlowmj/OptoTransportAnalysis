import pandas
import os
import matplotlib.pyplot as plt
from .data import Data

class TransportData(Data):
    # Base class for all transport data types. Initializes with connection to a 
    # database file containing sweep data and a metadata file containing instrument 
    # parameters for child classes to use.
    def __init__(self, fn="", fn_md=""):
        super().__init__(filename=fn, filename_md=fn_md)
        return
        
# Making child classes of TransportData for different parameter sweeps to make plotting more automated?
'''
class FieldSweep(TransportData):
    # Child class of TransportData for magnetic field sweeps.
    pass

class CurrentSweep(TransportData):
    # Child class of TransportData for bias current sweeps.
    pass

class GateSweep(TransportData):
    # Child class of TransportData for gate voltage sweeps.
    pass
'''
                
from os import path
import string
from .Data import Data

class OpticsData(Data):
    """
    Class containing spectral data and associated metadata.

    Contains specific methods pertinent to optical signals, 
    e.g., averaging spectra to elimiinate cosmic ray signals, converting 
    wavelength units to photon energy, etc.

    Attributes
    ----------

    data : pandas DataFrame
        Inherited from Data class. Dataframe containing spectral data, 
        collection wavelength, and other relevant information.

    metadata : dict, optional
        Inherited from Data class. dict containing relevant experimental
        information, e.g., exposure time, excitation laser, optical
        components used, etc.

    filename, filename_md : path or path-like str
        Inherited from Data class. A reference to the file used to 
        initialize the data or metadata attributes (if given).

    Methods
    -------

    add_average_signal()
        Appends the average intensity of spectra contained in data to data.
    
    """

    #### Constructor ---------------------------------------------------------

    def __init__(self, fn: path or string = None, fn_md: path or string = None,
        in_dir: path or string = "") -> None: 
        super().__init__(filename=fn, filename_md=fn_md, init_dir=in_dir)
        return

    #### Methods -------------------------------------------------------------

    def add_average_signal(self) -> None:
        """
        Adds an entry to the data attribute containing the average of all intensities.
        Does so without correcting for cosmic rays.
        """
        int_col_names = []
        for col_name in self.data.columns:
            if col_name.startswith('Intensity'):
                int_col_names.append(col_name)
        self.data['Average Intensity'] = self.data[int_col_names].sum(axis=1).values / self.metadata['num_frames']
        return

    
    


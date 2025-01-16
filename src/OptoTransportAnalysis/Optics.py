from os import path
import string
from .Data import Data
from scipy.constants import speed_of_light, Planck, electron_volt, pi
from scipy.fft import rfft, irfft
from scipy.signal import convolve
from scipy.special import chebyt
from numpy import array, cos, sum, gradient, mean

global defined_sum_cosine_windows
defined_sum_cosine_windows = {'Hann' : [0.5, 0.5, 0, 0, 0], 
                              'Hamming' : [25/46, 1-25/46, 0, 0, 0], 
                              'Blackman' : [0.42, 0.5, 0.08, 0, 0],
                              'Blackman (exact)' : [7938/18608, 9240/18608, 1430/18608, 0, 0], 
                              'Nuttall' : [0.355768, 0.487396, 0.144232, 0.012604, 0], 
                              'Blackman-Nuttall' : [0.3635819, 0.4891775, 0.1365995, 0.0106411, 0], 
                              'Blackman-Harris' : [0.35875, 0.48829, 0.14128, 0.01168, 0], 
                              'Flat top' : [0.21557895, 0.41663158, 0.277263158, 0.083578947, 0.006947368], 
                              'Custom' : []}

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

    metadata_flag : bool


    Methods
    -------
    add_average_signal()
        Appends the average intensity of spectra contained in data to data.
    
    """

    #### Constructor ---------------------------------------------------------

    def __init__(self, filename: string = None, filename_md: string = None,
        init_dir: string = "", metadata_flag = False) -> None: 
        super().__init__(filename=filename, filename_md=filename_md, init_dir=init_dir, 
                         metadata_flag=metadata_flag)
        return

    #### Methods -------------------------------------------------------------

    def add_average_signal(self, num_frames=None) -> None:
        """
        Adds an entry to the data attribute containing the average of all 
        intensities. Does so without correcting for cosmic rays.
        """
        int_col_names = [names for names in self.data.columns if names.startswith('Intensity')]
        num_frames = len(int_col_names)
        self.data['Average Intensity'] = self.data[int_col_names].sum(axis=1).values / num_frames
        return
    
    def add_eV_from_wavelength(self) -> None:
        """
        Adds an entry to the data giving the collected photon energy in eV from
        the collected wavelength.
        """
        self.data['Energy'] = self.data['Wavelength'].multiply(1e-9).pow(-1).multiply(Planck).multiply(speed_of_light).divide(electron_volt)
        return
    
    def apply_lpf(self, key_name, n_trunc) -> None:
        """
        Applies an ideal low-pass filter to the signal given by key_name.
        """
        fft_vals = rfft(self.data[key_name].values)
        fft_vals[n_trunc:] = 0
        self.data[key_name+' (FFT Smoothed)'] = irfft(fft_vals)
        return

    def apply_lpf_avg(self, n_trunc) -> None:
        """
        Applies an ideal low-pass filter to the 'Average Intensity' signal,
        if available.
        """
        assert('Average Intensity' in self.data.keys), 'No \'Average Intensity\' data available'
        self.fft_smooth('Average Intensity', n_trunc)
        return
    
    def apply_sum_cosine_window(self, key_name, window_name, N, alpha0=0, alpha1=0, alpha2=0, alpha3=0, alpha4=0) -> None:
        """
        Applies a sum-of-cosine window to the signal given by key_name. 
        Can choose from one of pre-defined windows:
        * Hann
        * Hamming
        * Blackman
        * Blackman (exact)
        * Nuttall
        * Blackman-Nuttall
        * Blackman-Harris
        * Flat top
        Or, make your own!

        Parameters
        ----------
        key_name : str
            Name of key corresponding to signal you wish to filter

        window_name : str
            Name of window/filter you wish to apply

        N : int
            Size of the window for filtering

        alpha0, alpha1, alpha2, alpha3, alpha4 : float, default=0
            Filter coefficients -- automatically populated unless 'Custom'
            is chosen

        Returns
        -------
        N/A
        """
        assert(window_name in defined_sum_cosine_windows.keys()), "Selected window not a valid choice"
        if window_name != 'Custom':
            [alpha0, alpha1, alpha2, alpha3, alpha4] = defined_sum_cosine_windows[window_name]
        sig = self.data[key_name].values
        window = alpha0 - alpha1*cos(array(range(N))*2*pi/N) + alpha2*cos(array(range(N))*4*pi/N) - alpha3*cos(array(range(N))*6*pi/N) + alpha4*cos(array(range(N))*8*pi/N)
        self.data[key_name + ' (' + window_name + ')'] = convolve(sig, window, mode='same') / sum(window)
        return
    
    def apply_sum_cosine_window_avg(self, window_name, cutoff, alpha0=0, alpha1=0, alpha2=0, alpha3=0, alpha4=0) -> None:
        """
        Applies a sum-cosine window to the 'Average Intensity' signal, if
        available.
        """
        assert('Average Intensity' in self.data.keys()), 'No \'Average Intensity\' data available'
        self.apply_sum_cosine_window('Average Intensity', window_name, cutoff, alpha0, alpha1, alpha2, alpha3, alpha4)
        return
    
    def compute_gradient(self, key_name) -> None:
        """
        Computes the gradient of the signal along the independent axis direction.
        """
        assert(key_name in self.data.keys()), 'Selected key not valid'
        self.data[f'Grad {key_name}'] = gradient(self.data[f'{key_name}'])
        return
    
    def compute_dR(self, key_name, background, subtract_mean = True) -> None:
        """
        Computes dR/R of the signal with respect to a given background.
        """
        spec = self.data[key_name].divide(self.data[key_name] + background.data['Intensity'])
        if subtract_mean:
            self.data[f'dR/R {key_name}'] = spec - mean(spec)
        else:
            self.data[f'dR/R {key_name}'] = spec
        return
from os import path
from pandas import Series
import string
from .Data import Data


class TransportData(Data):
    """
    Class containing transport data (or RMCD/other photodiode-collected data?) 
    and associated metadata.

    Contains specific methods pertinent to transport signals (and other 
    signals which form a line trace like those collected by a photodiode?), 
    e.g. integration, MCA coefficient calculation, calculating resistance, etc.

    Attributes
    ----------

    data : pandas DataFrame
        Inherited from Data class. Dataframe containing transport data, 
        sweep parameters, and other relevant information.

    metadata : dict, optional
        Inherited from Data class. dict containing relevant experimental
        information, e.g., amplfier gain, amplifier sensitivity, lock-in 
        parameters, etc.

    filename, filename_md : path or path-like str
        Inherited from Data class. A reference to the file used to 
        initialize the data or metadata attributes (if given).

    Methods
    -------

    __init__(fn=None, fn_md=None, in_dir="")
        Constructor. Uses Data constructor, see Data.py for documentation.

    get_RTcond_DilFridge(exp_name, start_time=0, warm=False)
        Obtain a Series of boolean values used to clean up RT curves
        from the dilution fridge, which is highly prone to hysteresis
        as it cools and warms.

    append_resistance_signal(exp_name, R_name, V_sig_name, I_sig_name, 
                             gain=None, sensitivity=None)
        Add a resistance signal to the given experiment's data according 
        to the voltage and current given by V_sig_name and I_sig_name 
        with optional parameters for multiplicative factors from experimental
        devices.

    append_MCA_coefficient(exp_name, MCA_name, R_2f_sig, R_f_sig, B_sig, 
                               I_sig, gain=None, sensitivity=None)
        Add a series containing the non-reciprocal transport coefficient
        to the given experiment's data using a given 2f and 1f resistance
        with AC current & magnetic field, as well as optional parameters 
        for multiplicative factors from experimental devces.

    append_symm_antisymm_rho(exp_name, R_sig)
        Compute and append a symmetrized and antisymmetrized resistance 
        signal to given experiment's data. 
        
    """

    #### Constructor ---------------------------------------------------------

    def __init__(self, fn: path or string = None, fn_md: path or string = None,
        in_dir: path or string = "") -> None:
        super().__init__(filename=fn, filename_md=fn_md, init_dir=in_dir)
        return

    #### Methods -------------------------------------------------------------

    def get_RTcond_DilFridge(self, exp_name: string, start_time: float = 0, 
            warm: bool = False):
        """
        Returns a Series of True/False conditions for a RT curve from one of the 
        dilution fridges to give a clean RT curve.

        Parameters
        ----------

        exp_name : str
            Name of the experiment containing the RT curve.

        start_time : float, default=0
            Time value at which to start computing. Useful for warming 
            curves, long scans which include warming and cooling, 
            scans from temperatures above 100K, etc.

        warm : bool, default=False
            Whether the curve being analyzed is from warming or cooling.
            Affects the logic which yields the return value.
        
        Returns
        -------

        less_than_all_prev : Series[bools]
            pandas Series containing boolean conditional values for 
            each point in given Series/DataFrame object (RT curve) such
            that, when plotted, the values corresponding to those which 
            are True in less_than_all_prev will be monotonically 
            increasing/decreasing depending on direction of sweep 
            parameter (temperature).

        """
        if warm:
            greater_than_all_prev = self.data[exp_name]["lakeshore_372_ch09_temperature"][start_time:] > self.data[exp_name]["lakeshore_372_ch09_temperature"][start_time:].cummax().shift().astype(float)
            return greater_than_all_prev
        else:
            less_than_all_prev = self.data[exp_name]["lakeshore_372_ch09_temperature"][start_time:] < self.data[exp_name]["lakeshore_372_ch09_temperature"][start_time:].cummin().shift().astype(float)
            return less_than_all_prev

    def append_resistance_signal(self, exp_name: string, R_name: string, 
            V_sig_name: string, I_sig_name: string, gain: float = None, 
            sensitivity: float = None) -> None:
        """
        Appends a resistance signal to given data object.

        Parameters
        ----------

        exp_name : str
            Name of the experiment containing the relevant voltage and 
            current signals.

        R_name : str
            Proposed name for the resistance signal to be appended.

        V_sig_name, I_sig_name : str
            Name of the voltage and current signals to be used to 
            compute resistance.

        gain : float, optional
            Optional parameter for pre-amplifier gain if one was used
            to multiply and clean the signal for the experiment.

        sensitivity : float, optional
            Optional parameter for current amplifier sensitivity if one
            was used to convert ouptut current of device to voltage.

        Returns
        -------

        N/A
 
        """
        R_signal = self.data[exp_name][V_sig_name] / self.data[exp_name][I_sig_name]
        if gain != None:
            R_signal = R_signal / self.metadata[gain]
        if sensitivity != None:
            R_signal = R_signal / self.metadata[sensitivity]
        self.data[exp_name][R_name] = R_signal
        return
        
    def append_MCA_coefficient(self, exp_name: string, MCA_name: string, 
            R_2f_sig: string, R_f_sig: string, B_sig: string or float, 
            I_sig: string, gain: float = None, sensitivity: float = None) -> None:
        """
        Appends a series containing the non-reciprocal transport 
        coefficient γ to the given data. Can be computed as a function 
        of fixed or swept magnetic field.

        Parameters
        ----------

        exp_name : str
            Name of the experiment containing the relevant resistance,
            current, and magnetic field signals/values.

        MCA_name : str
            Proposed name for MCA signal to be appended to the data.

        R_2f_sig, R_f_sig, I_sig : str
            Name of R_2f, R_f, and current signals used for the computation.

        B_sig : str or float
            Name of magnetic field sweep parameter OR value of fixed
            magnetic field at which scan was taken.

        gain, sensitivity : float, optional
            Optional parameters for the gain of any pre-amplifiers not
            taken into account when computing the resistance signals and
            the sensitivity of any current amplifier used.

        Returns
        -------

        N/A

        Notes
        -----

        The non-reciprocal transport coefficient, also called the coefficient
        of magnetochiral anisotropy (MCA), is defined as

            γ = R_2f / (R_f * B * I_SD)

        Where I_SD is the applied AC source-drain current at frequency f,
        R_2f is the non-reciprocal/non-linear transport signal measured
        at frequency 2f, R_f is the sheet resistance of the sample measured
        at f, and B is the magnetic field. Typical units of γ are 1/(Tesla*Amp).
        This quantity is interesting to determine as a function of temperature.
        Error bars can be generated by performing statistics on the generated
        Series. For more information, check
        https://www.science.org/doi/10.1126/sciadv.1602390

        """
        MCA = self.data[exp_name][R_2f_sig] / self.data[exp_name][R_f_sig] / self.data[exp_name][I_sig]
        
        # Check if B_sig given is fixed value or swept parameter
        if type(B_sig) is float:
            MCA = MCA / B_sig
        else:
            MCA = MCA / self.data[exp_name][B_sig]
        
        # Take optional parameters into account
        if gain != None:
            MCA = MCA / gain
        if sensitivity != None:
            MCA = MCA / sensitivity

        self.data[exp_name][MCA_name] = MCA
        return

    def append_symm_antisymm_rho(self, exp_name: string, R_sig: string) -> None:
        """
        Appends the symmetrized and anti-symmetrized parts of a resistance
        signal to the given data.

        Names the symmetrized and anti-symmetrized signals after the given
        resistance signal with the suffixes "_symm" and "_antisymm".

        Parameters
        ----------

        exp_name : str
            Name of the experiment containing the relevant resistance signal.

        R_sig : str
            Name of the resistance signal to be symmetrized and anti-
            symmetrized.

        Returns
        -------

        N/A
        """
        self.data[exp_name][R_sig + "_symm"] = (self.data[exp_name][R_sig] + self.data[exp_name][R_sig].iloc[::-1]) / 2
        self.data[exp_name][R_sig + "_antisymm"] = (self.data[exp_name][R_sig] - self.data[exp_name][R_sig].iloc[::-1]) / 2
        return
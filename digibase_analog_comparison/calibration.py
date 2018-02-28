import numpy as np
import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit
#from modelling import gauss
import statsmodels.api as sm
from lmfit.models import GaussianModel
from lmfit.models import LinearModel

def data_clean(data_2_calibrate, clean_right):
    '''
    The while loop goes through and identifies the largest peak in the
    spectrum and it records the position of that peak. It then removes
    the peak by removing 10 channels from the right and left of the peak.
    The code will then search for the next largest position.
    '''

    list_data = np.array(data_2_calibrate).tolist()
    iterator = 0
    while iterator < (clean_right):
        list_data[iterator] = 0
        iterator += 1
    '''
    merging the data for the calibration
    Also converting merged data into a list so channels can be
    removed easier.
    '''
    return list_data

def spectrum_calibration(channel_width, energy_list, spectrum_data, clean_right):

    '''
    The while loop goes through and identifies the largest peak in the
    spectrum and it records the position of that peak. It then removes
    the peak by removing 10 channels from the right and left of the peak.
    The code will then search for the next largest position.
    '''

    list_data = np.array(spectrum_data).tolist()
    iterator = 0
    while iterator < (clean_right):
        list_data[iterator] = 0
        iterator += 1
    '''
    merging the data for the calibration
    Also converting merged data into a list so channels can be
    removed easier.
    '''
    data_2_calibrate = list_data
    i = 0; channel_max_list = []; gauss_x = []; gauss_y = []
    fit_channel = []
    while i < len(energy_list):
        channel_max = np.argmax(data_2_calibrate)
        data_left = channel_max - channel_width
        data_right = channel_max + channel_width
        channel_max_list.append(channel_max)
        iterator = data_left
        while iterator < (data_right):
            data_2_calibrate[iterator] = 0
            iterator += 1
        i += 1

    '''
    sorting channel number so the correct channel number corresponds with
    the correct energy.
    '''
    channel_number = sorted(channel_max_list, key=int)
    energy = energy_list
    results = sm.OLS(energy,sm.add_constant(channel_number)).fit()

    slope, intercept = np.polyfit(channel_number, energy, 1)

    abline_values = [slope * i + intercept for i in channel_number]

    return slope, intercept

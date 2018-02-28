from becquerel import Spectrum
import numpy as np
import matplotlib.pyplot as plt
import os
from copy import deepcopy
from gamma_energies import gamma_energies
from calibration import spectrum_calibration
from lmfit.models import GaussianModel
from lmfit.models import LinearModel
import operator
import math

'''
spectrum_gauss_fit takes an input spectrum and finds the peaks of the
spectrum and fits a gaussian curve to the photopeaks
'''
def spectrum_gauss_fit(real_data, clean_right, channel_width, energy_spectrum, cal):

    '''
    The while loop goes through and identifies the largest peak in the
    spectrum and it records the position of that peak. It then removes
    the peak by removing 10 channels from the right and left of the peak.
    The code will then search for the next largest position.
    '''

    list_data = np.array(real_data).tolist()
    iterator = 0
    while iterator < clean_right:
        list_data[iterator] = 0
        iterator += 1
    '''
    merging the data for the calibration
    Also converting merged data into a list so channels can be
    removed easier.
    '''
    spectrum_data = np.array(real_data).tolist()

    '''
    Attempting to iterate through the peaks and identify all of the peaks
    for plotting purposes. All of the peaks are found from the trimmed data
    and the corresponding count rates are found. A list is created and then the
    list is sorted based by the position of the counts.
    '''
    i = 0; energy_list_2 =[]
    gauss_x =[]; gauss_y=[]; real_y_gauss =[]
    parameter_list_2 = []; gauss_fit_parameters = []
    sigma_list = []; amplitude_list =[]; fit_params = {}

    while i < len(energy_spectrum):
        channel_max = np.argmax(list_data)
        energy_list_2.append(list_data[channel_max])
        data_left = channel_max - channel_width
        data_right = channel_max + channel_width
        '''
        Instead of deleting the items from the list. I am placing them to
        zero. The while loop iterates over the peak and sets it to zero.
        I am still using a place holder in the real data so the zero's do
        not obscure my fits.
        '''
        calibration = []
        iterator = data_left
        while iterator < (data_right):
            calibration.append(cal[iterator])
            gauss_x.append(iterator)
            gauss_y.append(list_data[iterator])
            real_y_gauss.append(spectrum_data[iterator])
            list_data[iterator] = 0
            iterator += 1
        x = np.asarray(calibration)
        y = np.asarray(gauss_y)
        print("The amplitude sum is %0.2f" % sum(y))
        real_y = np.asarray(real_y_gauss)
        '''
        information for plotting the Gaussian function.
        '''
        mod_gauss  = GaussianModel(prefix='g1_')
        line_mod = LinearModel(prefix='line')
        pars = mod_gauss.guess(real_y, x=x)
        pars.update(line_mod.make_params(intercept=y.min(), slope=0))
        pars.update(mod_gauss.make_params())
        pars['g1_center'].set(x[np.argmax(real_y)], min=x[np.argmax(real_y)]\
        - 3)
        pars['g1_sigma'].set(3, min=0.25)
        pars['g1_amplitude'].set(max(real_y), min=max(real_y)-10)
        mod = mod_gauss + line_mod
        out  = mod.fit(real_y, pars, x=x)

        plt.plot(x,real_y)
        plt.plot(x, out.best_fit, 'k--')
        energy_title = np.argmax(x)
        max_y = np.argmax(real_y)  # Find the maximum y value
        max_x = x[(max_y)]  # Find the x value corresponding to the maximum y value
        #plt.title('Gaussian fit around %0.1f keV' % x[max_y])
        plt.xlabel('Channel Number')
        plt.ylabel('CPS')
        gauss_x = []; gauss_y = []; parameter_list_1 = []
        real_y_gauss =[]
        plt.show()
        i += 1
        #print(out.fit_report(min_correl=10))
        sigma = out.params['g1_sigma'].value
        amplitude = out.params['g1_amplitude'].value
        sigma_list.append(sigma); amplitude_list.append(amplitude)
        fit_params = {}


        #gauss_fit_parameters = [out.params[key].value for k in out.params]
        #print(key, "=", out.params[key].value, "+/-", out.params[key].stderr)
        parameter_list_2.append(out)
        gauss_fit_parameters = []
    '''
    The below line sorts the channels by energy_list_2
    '''

    #energy_channel = list(zip(channel_max_list, energy_list_2, parameter_list_2))
    #energy_channel.sort(key=operator.itemgetter(0))
    plt.clf()

    '''
    This sequence plots the energy of the peaks and with their corresponding
    energies.
    '''
    return out

#def fit_gauss_line():

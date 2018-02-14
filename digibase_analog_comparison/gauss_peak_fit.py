'''
spectrum_gauss_fit takes an input spectrum and finds the peaks of the
spectrum and fits a gaussian curve to the photopeaks
'''
def spectrum_gauss_fit(bgsub_array, clean_left, clean_right, channel_width, energy_spectrum, slope_d, intercept_d):
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

    y_counts = bgsub_array

    list_data = np.array(y_counts).tolist()
    iterator = clean_left
    while iterator < (clean_right):
        list_data[iterator] = 0
        iterator += 1
    '''
    merging the data for the calibration
    Also converting merged data into a list so channels can be
    removed easier.
    '''
    data_2_calibrate = list_data

    '''
    Attempting to iterate through the peaks and identify all of the peaks
    for plotting purposes. All of the peaks are found from the trimmed data
    and the corresponding count rates are found. A list is created and then the
    list is sorted based by the position of the counts.
    '''
    i = 0; channel_max_list = []; energy_list_2 =[]
    gauss_x =[]; gauss_y=[]; fit_channel = []
    parameter_list_2 = []

    while i < len(energy_spectrum):
        channel_max = np.argmax(list_data)
        channel_max_list.append(channel_max)
        energy_list_2.append(list_data[channel_max])
        data_left = channel_max - channel_width
        data_right = channel_max + channel_width
        '''
        Instead of deleting the items from the list. I am placing them to
        zero. The while loop iterates over the peak and sets it to zero.
        '''
        iterator = data_left
        while iterator < (data_right):
            gauss_x.append(iterator)
            gauss_y.append(list_data[iterator])
            x = np.asarray(gauss_x)
            y = np.asarray(gauss_y)
            fit_channel.append(list_data[iterator])
            list_data[iterator] = 0
            iterator += 1
        '''
        information for plotting the Gaussian function.
        '''
        mod  = GaussianModel(prefix='g1_')
        line_mod = LinearModel(prefix='line')
        pars = mod.guess(y, x=x)
        pars.update(line_mod.make_params(intercept=y.min(), slope=0))
        pars.update( mod.make_params())
        pars['g1_center'].set(gauss_x[np.argmax(gauss_y)], min=gauss_x[np.argmax(gauss_y)]\
        - 3)
        pars['g1_sigma'].set(3, min=0.25)
        pars['g1_amplitude'].set(max(gauss_y), min=max(gauss_y)-10)
        mod = mod + line_mod
        out  = mod.fit(y, pars, x=x)
        count_first = float(x[0])
        count_last = float(x[-1])
        calibrated_channel = []
        while count_first <= count_last:
            calibrated_channel += [count_first*slope_d+ intercept_d]
            count_first += 1
        calibrated_channel = np.asarray(calibrated_channel, 'float')
        plt.plot(calibrated_channel,y)
        plt.plot(calibrated_channel, out.best_fit, 'k--')
        energy_title = np.argmax(calibrated_channel)
        plt.title('Gaussian fit to %0.2f keV' % energy_spectrum[i])
        plt.xlabel('Energy (keV)')
        plt.ylabel('Counts')
        gauss_x = []; gauss_y = []; fit_channel = []; parameter_list_1 = []
        plt.show()
        i += 1
        #print(out.fit_report(min_correl=10))
        for key in out.params:
            #print(key, "=", out.params[key].value, "+/-", out.params[key].stderr)
            parameter_list_1.append(out.params[key].value)
        parameter_list_2.append(parameter_list_1)
    '''
    The below line sorts the channels by energy_list_2
    '''
    energy_channel = list(zip(channel_max_list, energy_list_2, parameter_list_2))
    energy_channel.sort(key=operator.itemgetter(0))
    plt.clf()

    '''
    This sequence plots the energy of the peaks and with their corresponding
    energies.
    '''
    #fig = plt.figure()
    #energy_list_2 =[]
    #for channel, energy in energy_channel:
    #    energy_list_2.append(float(energy))
    #for x, y in zip(energy_spectrum, energy_list_2):
    #    x1 = np.linspace(x,x, 10000)
    #    y1 = np.linspace(100, 1000,10000)
    #    p1 = plt.plot(x1,y1, 'b', linestyle = '--', zorder = 10)
        #plt.annotate('%0.1f keV' % x, xy=(x, y+50), xytext=(x, y+50))
    #    plt.xlim(0, max(energy_spectrum)+100, 100)
    #plt.semilogy(calibrated_channel, y_counts, 'k', zorder = 0)
    #plt.ylabel("Counts")
    #plt.xlabel("Energy(keV)")
    #plt.title("Calibrated Energy Plot - Digital")
    return energy_channel

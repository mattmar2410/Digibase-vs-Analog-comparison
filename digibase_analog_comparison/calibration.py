def spectrum_calibration(channel_width, energy_list, data_2_calibrate):
    import numpy as np
    import matplotlib.pyplot as plt
    #from scipy.optimize import curve_fit
    #from modelling import gauss
    import statsmodels.api as sm
    from lmfit.models import GaussianModel
    from lmfit.models import LinearModel

    '''
    The while loop goes through and identifies the largest peak in the
    spectrum and it records the position of that peak. It then removes
    the peak by removing 10 channels from the right and left of the peak.
    The code will then search for the next largest position.
    '''

    i = 0; channel_max_list = []; gauss_x = []; gauss_y = []
    fit_channel = []
    while i < len(energy_list):
        channel_max = np.argmax(data_2_calibrate)
        data_left = channel_max - channel_width
        data_right = channel_max + channel_width
        channel_max_list.append(channel_max)
        iterator = data_left
        while iterator < (data_right):
            gauss_x.append(iterator)
            gauss_y.append(data_2_calibrate[iterator])
            x = np.asarray(gauss_x)
            y = np.asarray(gauss_y)
            fit_channel.append(data_2_calibrate[iterator])
            data_2_calibrate[iterator] = 0
            iterator += 1
        i += 1
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
        gauss_x = []; gauss_y = []; fit_channel = []
        #print(out.fit_report(min_correl=10))
        #for key in out.params:
        #    print(key, "=", out.params[key].value, "+/-", out.params[key].stderr)

    '''
    sorting channel number so the correct channel number corresponds with
    the correct energy.
    '''
    channel_number = sorted(channel_max_list, key=int)
    energy = energy_list
    results = sm.OLS(energy,sm.add_constant(channel_number)).fit()

    slope, intercept = np.polyfit(channel_number, energy, 1)

    abline_values = [slope * i + intercept for i in channel_number]
    #plt.plot(channel_number,energy, 'ro')
    #plt.plot(channel_number, abline_values, 'b')
    #plt.xlabel('Channel Number')
    #plt.ylabel('Energy [keV]')
    #plt.title('Best Fit Line')
    return slope, intercept

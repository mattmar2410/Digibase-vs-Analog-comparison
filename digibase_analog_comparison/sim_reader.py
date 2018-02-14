def cosima_output(fname):
    import numpy as np
    import matplotlib.pyplot as plt
    figure_counter=0; count_list = []; bin_centers_list = []
    energies = [];l_old = ""; counter = 0; iterator = 0
    with open(fname, 'r') as infile:
        for i, l in enumerate(infile):
            if l.startswith('HTsim') and l_old.startswith('HTsim'):
                #==============
                #Checking to see if there were multiple hits from a single particle in the detector
                #If there were multiple countes, the energies of the particles are summed together
                #==============
                data = [x.strip() for x in l.split(';')]  # break on `;` and strip whitespace
                energy_update = float(data[4])
                energy_keV = energy_old + energy_update #updating the energy to the sum of the particles
                energies[iterator-counter] = (energy_keV) #updates the list of energies and replaces the previous
                #energy with the new summed energy
                energy_old = energy_keV
                counter+=1
            elif l.startswith('HTsim'):
                data = [x.strip() for x in l.split(';')]  # break on `;` and strip whitespace
                energy_keV = float(data[4])
                energy_old = energy_keV #storing the current energy as the new old energy
                l_old = str(data[0])
                energies.append(energy_keV)
                counter+=1
                iterator+=1
            else:
                #================
                #Initializing all of the variables back to 0 since HTsim was not hit
                #=========
                l_old = ""
                energy = 0
                counter = 0
            if i % 100000 == 0:
                print(i)
        nrg = np.array(energies)
        counts, bin_edges = np.histogram(nrg, bins=1000)
        bin_centers = (bin_edges[1:]+bin_edges[:-1])/2
        counts, bin_edges = np.histogram(nrg, bins=np.linspace(0, max(energies)+100))
        count_list.append(counts)
        bin_centers = (bin_edges[1:]+bin_edges[:-1])/2
        bin_centers_list.append(bin_centers)
    return bin_centers, counts

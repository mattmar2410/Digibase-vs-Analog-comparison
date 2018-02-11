#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 13:40:59 2017

@author: Matt
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 09:46:48 2017

@author: Matt Marshall
Finds average mass for the elements:

*    mass, mass_units (u)
         The molar mass averaged over natural isotope abundance.

Atomic Weights and Isotopic Composition [#Coursey]_.

The atomic weights are available for elements 1 through 112, 114, & 116 and
isotopic compositions or abundances are given when appropriate. The atomic
weights data were published by Coplen [#Coplen]_ in Atomic Weights of the
Elements 1999, (and include changes reported from the 2001 review in
Chem. Int., 23, 179 (2001)) and the isotopic compositions data were
published by Rosman [#Rosman]_ and Taylor [#Taylor]_ in Isotopic Compositions
of the Elements 1997.  The relative atomic masses of the isotopes data were
published by Audi [#Audi]_ and Wapstra [#Wapstra]_ in the 1995 Update To The
Atomic Mass Evaluation.

This data has been compiled from the above sources for the user's convenience
and does not represent a critical evaluation by the NIST Physics Laboratory.
http://physics.nist.gov/PhysRefData/Compositions/

Neutron mass from NIST Reference on Constants, Units, and Uncertainty
http://physics.nist.gov/cuu/index.html

.. [#Coursey] Coursey. J. S., Schwab. D. J., and Dragoset. R. A., NIST,
       Physics Laboratory, Office of Electronic Commerce in Scientific
       and Engineering Data.
.. [#Coplen] Coplen. T. B. : U.S. Geological Survey, Reston, Virginia, USA.
.. [#Rosman] Rosman. K. J. R. : Department of Applied Physics, Curtin University
       of Technology, Australia.
.. [#Taylor] Taylor. P. D. P. : Institute for Reference Materials and
       Measurements, European Commission, Belgium.
.. [#Audi] Audi. G. : Centre de Spectrométrie Nucléaire et de Spectrométrie
       de Masse, Orsay Campus, France.
.. [#Wapstra] Wapstra. A. H. : National Institute of Nuclear Physics
       and High-Energy Physics, Amsterdam, The Netherlands.
"""
import re
from sys import argv

#Make user_input an array that handles all of the elements for number density
#Create a for loop that iterates over the whole program for those entered
#elements. You will want to use something that looks for commas that separate
#the elements.
def gamma_energies (*args):
    import numpy as np
    fname = './gamma_energies.txt'
    '''
    number_density (*args) -- returns the number_density in atoms/cc.
    The function handles as many entries as the user wants to input. Separate
    each element with a comma.
    Example number_density ("U235", "H2"); number_density ("O", "H2") - it would
    use the average weight of oxygen and the atomic mass for H2
    '''
    i=0; energy_list = []; Isotope_label = []; iso_mass_value_list = []
    while i < len(args):
        f = open(fname, "r") #opens the file name
        user_input = str(args)
        #x splits all three user inputs
        x = user_input.split(",") #splitting the user_input into separate entries
        """
        numeric and rx separate the isotope number from the element.
        i.e. U235 returns just 235
        """
        numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
        rx = re.compile(numeric_const_pattern, re.VERBOSE)
        """
        iso_mass_value uses the iterator i to grab one isotope separately
        for each iteration
        """
        iso_mass_value = rx.findall(x[i])

        """
        isotope name finds the upper and lowercase letters for the entry
        """
        isotope_name_U=''.join([c for c in x[i] if c.isupper()])
        isotope_name_L=''.join([c for c in x[i] if c.islower()])
        isotope_name=isotope_name_U+isotope_name_L
        iso_mass_value = str(''.join(iso_mass_value))

        """
        Reads through Isotope_properties_NIST.txt and returns the atomic mass value
        The first if statement finds the isotope name in the line
        Then it searches if the isotope number matches i.e 235=235. It proceeds
        to pull all the relevant information
        """
        f = open(fname)
        ## Read the first line
        line = f.readline()
        while line:
            line = f.readline()
            try:
                isotope, energy = line.split()
                el, sym, iso = isotope.split('-')
                if isotope_name in line:
                    if iso_mass_value == iso:
                        energy = float(energy)
                        energy_list.append(energy)
                        #print(energy_list)
                        Isotope_label.append(isotope_name)
                        iso_mass_value_list.append(iso_mass_value)
                        #print ("the energy of %s%s = %f " % (isotope_name, iso_mass_value, energy))
            except ValueError:
                pass
            if line == '': #Reads until end of file
                break
        i += 1
    f.close()
    return energy_list

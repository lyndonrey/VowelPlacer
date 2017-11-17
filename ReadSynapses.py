#! /usr/bin/env python

import sys
import numpy as np

# Read synapses from text file in order to not have to retrain 
#   in order to debug
def readText(syn1fn, syn2fn):
    s0 = np.genfromtxt(syn1fn, dtype=float)
    # Matrix must be transposed or else matrix mult not possible
    s1 = np.array([np.genfromtxt(syn2fn, dtype=float)]).T
    return [s0, s1]
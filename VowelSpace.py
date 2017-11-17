#! /usr/bin/env python

import sys 
import numpy as numpy
import Learn
import ReadSynapses
import NotVowel

# Main method for whole process
# True as arg 1 means train, false means read pretrained synapses

# They could be converted to bool but not really necessary
if sys.argv[1] == "True":
    synapsesIn = Learn.main()
elif sys.argv[1] == "False":
    synapsesIn = ReadSynapses.readText(sys.argv[1], sys.argv[2])
else:
    print("Invalid param for arg 1")

# Test each data sample to gsee where each sample places after NN output
Learn.testMatrix(synapsesIn[0], synapsesIn[1], "out-FAE-G01_3-75-50.csv", "whole_test.csv", 0.001)
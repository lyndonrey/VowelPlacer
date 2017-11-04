#! /usr/bin/env python
import sys
import numpy as np


# Sigmoid activation function
def nonlin(x, deriv=False):
    if (deriv):
        return x*(1-x)
    return 1 / (1+np.exp(-x))



# Scrape data from text file from praat
def getData(fn):
    with open(fn) as f:
        fLines = f.readlines()
        data = np.loadtxt(fLines)
        # Scale the data to prevent overflows
        dataScaled = np.multiply(data, np.array([0.0001]))
    return dataScaled



def learn(X, out, alpha, iterations, layers):
    synapse0 = 2*np.random.random((5, layers)) - 1  
    synapse1 = 2*np.random.random((layers, 1)) - 1

    XunionY = np.concatenate((X, np.random.rand(100,5)), axis=0)    
    for i in range(iterations):
        #if i % 100 == 0:
        #    Y = np.random.rand(100,2)
        #    XunionY = np.concatenate((X,Y), axis=0)

        # sample in
        #vowel = np.array([X[i%X.shape[0],0:]])
        layer0 = XunionY[[i % np.shape(XunionY)[0]]]
        layer1 = nonlin(np.dot(layer0, synapse0))
        layer2 = nonlin(np.dot(layer1,synapse1))

        # how much did we miss?
        l2_error = out[[i % np.shape(out)[0]]] - layer2

        if (i % 10000) == 0:
                print("At \033[93m", i, "\033[0m iterations, error rate is: ", '\033[93m', str(np.mean(np.abs(l2_error))), '\033[0m')
    
        # multiply how much we missed by the
        # slope of the sigmoid at the values in l1
        l2_delta = l2_error * nonlin(layer2, True)

        l1_error = l2_delta.dot(synapse1.T)

        l1_delta = l1_error * nonlin(layer1, True)
    
        # update weights
        synapse1 += np.dot(layer1.T, l2_delta)
        synapse0 += np.dot(layer0.T, l1_delta)

        if (i % np.random.randint(9000,11000)) == 0:
            print("At \033[93m", i, "\033[0m iterations, error rate is: ", '\033[93m', str(np.mean(np.abs(l2_error))), '\033[0m')


    # return final synapses to test with
    with open("synapses.csv", "w") as text_file:
        text_file.write(str(synapse0))
        text_file.write(str(synapse1))
    return [synapse0, synapse1]



# Test the trained net
def test(X, s0, s1):
    l1 = nonlin(np.dot(X, s0))
    l2 = nonlin(np.dot(l1, s1))
    return l2


def frange(start, stop, step):
    x = start 
    while x < stop:
        yield x
        x += step

def testMatrix(s0, s1):
    count = 0
    index = 0

    with open("whole_test.csv", "w") as text_file:
            scaledRaw = getData("out-FAE-HOMELAND_3-75-50.csv")
            i = 0
            j = 0
            for l in scaledRaw:
                print("Total samples analysed:", i, "Total samples accepted:", j, end='\r')
                if test(l, s0, s1) > 0.995:
                    text_file.write(str(l) + "\n")
                    j += 1 
                i += 1

X = getData('i.csv')

Xprime = np.ones((1000,1))
Yprime = np.zeros((100,1))
XprimeUnionYprime = np.concatenate((Xprime, Yprime), axis=0)

print(XprimeUnionYprime)
s = learn(X, XprimeUnionYprime, 0.1, 10000000, 10)

testMatrix(s[0], s[1])
#print(test([0.0190, 0.2050], s[0], s[1], s[2]))
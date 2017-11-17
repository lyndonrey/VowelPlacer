#! /usr/bin/env python

import sys
import Learn
import numpy as np

# Creates a negative training set for training NN
# Creates a text file with every possible sample value
#   in dataset, that is not specified vowel
def main():
    yesVowel = Learn.getData(sys.argv[1])
    
    with open("notVowel.csv", "w") as text_file:
        # This isn't super efficient, but functional enough for the time being
        for i in range(100, 600):
            for j in range(700, 2500): 
                #scale i and j
                ifloat = i / 10000
                jfloat = j / 10000
                flag = False
                for v in yesVowel:
                    print(float(v[0]), float(v[1]), ifloat, jfloat)
                    if float(v[0]) == ifloat and float(v[1]) == jfloat:
                        flag = True
                
                if not flag:
                    text_file.write(str(i) + " " + str(j) + "\n")


if __name__ == "__main__":
    main()

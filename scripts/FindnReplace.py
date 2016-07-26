import numpy as np
import csv

def getAverages(line):
    print line

    #some if statement doing our thing
    # http://stackoverflow.com/questions/19773669/python-dictionary-replace-values
    #sample dictionary = {'corse': 378, 'cielo': 209, 'mute': 16}


with open('name of input file.csv', 'rb') as csvfile:
    with open('name of output file.csv','wb') as f:
        writer = csv.writer(f,delimiter=',')
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:

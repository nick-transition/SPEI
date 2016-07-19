import pandas as pd
import numpy as np
import time
import csv

df = pd.read_csv('SPEI-test-time.csv')
head = pd.DataFrame(df.ix[2000:2005])
headDates = list(head.ix[:1,2:])
#Returns a list of lists
years = map(lambda w: [w.split('-')[0]], headDates)
#Flatten the list -> retrieve items in sublists in deep list
years = [int(item) for sublist in years for item in sublist]
setYears = sorted(list(set(years)))
numYears = len(setYears)
print setYears
#print 'Number of Years'

out = pd.DataFrame()
#Output csv define and open it here

#def writeLine(list):
    #get length of line

    #iterate through each item in list

    #switches to create appropriate averages

    # write line to new csv


# Split first 2 columns from dataset, grouby kind of fails and but time formatting works
#grp = df.ix[:,2:].groupby(lambda x: time.strptime(x,"%Y-%m-%d %H:%M:%S").tm_year,axis=1)

# Data lives here


#print(list(grp.columns.values))

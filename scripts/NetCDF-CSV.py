import netCDF4
from netCDF4 import Dataset, num2date, date2index
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import csv
import datetime

# NetCDF4-Python can read a remote OPeNDAP dataset or a local NetCDF file:
file='spei01.nc'
nc = netCDF4.Dataset(file)
nc.variables.keys()

lats = nc.variables['lat'][:]#[189:250]
lons = nc.variables['lon'][:]#[490:558]
time_var = nc.variables['time']
dtime = netCDF4.num2date(time_var[:],time_var.units)
times = nc.variables['time'][:]
units = nc.variables['time'].units


# specify some location to extract time series
lati = lats[189:250]; loni = lons[490:558]
#lati = lats[248:250]; loni = lons[550:558]


#print tim
#print(lati,loni,tim)
# find closest index to specified value
def near(array,value):
    idx=(abs(array-value)).argmin()
    return idx

def fixline(list1):
	return str(list1).replace("[","").replace("]","")

# Find nearest point to desired location (could also interpolate, but more work)
#ix = near(lons, loni)
#iy = near(lats, lati)

# Extract desired times.
start = dt.datetime(1990,1,1,0,0,0)
stop = dt.datetime(1994,1,1,0,0,0)


# these don't matter...need to use different indexing method on the DataFrame
istart = netCDF4.date2index(start,time_var,select='nearest')
istop = netCDF4.date2index(stop,time_var,select='nearest')

print istart,istop
#print(istart,istop)

# Get all time records of variable [vname] at indices [iy,ix]
vname = 'spei'

var = nc.variables[vname]

i=0
header = ['Index','Latitude', 'Longitude']
with open('SPEI-test-time.csv', 'wb') as csvFile:
    outputwriter = csv.writer(csvFile, delimiter=',')
    for time_index, time in enumerate(times[1067:]): #set to 1067: for 1990 to latest available
         t = num2date(time, units = units, calendar='365_day')
         header.append(t)
    outputwriter.writerow(header)

    for lat_index, lat in enumerate(lati):
        for lon_index, lon in enumerate(loni):
            print(lat,"-",lon)

            istart = netCDF4.date2index(start,time_var,select='nearest')
            data = var[istart:,near(lats,lat),near(lons,lon)]
            dstring = fixline(data.tolist())
            content = [i,lat,lon]+data.tolist()
            outputwriter.writerow(content)
            i +=1

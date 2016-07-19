from netCDF4 import Dataset, num2date
import datetime as dt

filename = "spei01.nc"

nc = Dataset(filename, 'r', Format='NETCDF4')

# get coordinates variables
lats = nc.variables['lat'][:]
lons = nc.variables['lon'][:]
#lats = (lat for lat in lats if lat > 5 and lat < 33)
#lons = (lon for lon in lons if lon > 66 and lon < 92)
spei= nc.variables['spei']
times = nc.variables['time']
# convert date, how to store date only strip away time?
print("Converting Dates")
units = nc.variables['time'].units
dates = num2date (times[:], units=units, calendar='365_day')

start = dt.datetime(2007,1,1,0,0,0)
stop = dt.datetime(2010,1,1,0,0,0)

istart = nc.date2index(start,times,select='nearest')
istop = nc.date2index(stop,times,select='nearest')

maxLat = 33; maxLon = 92

def near(array,value):
    idx=(abs(array-value)).argmin()
    return idx

iLat = near(lats,maxLat)
iLon = near(lons,maxLon)



print(spei[istart:istop,iLat,iLon])

# the csv file is closed when you leave the block


# close the output file
csvFile.close()

# close netcdf
nc.close()

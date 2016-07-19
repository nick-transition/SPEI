import numpy as np
import time
import csv

lats = []
lons = []
years = []


# This function accepts a range of SPEI values and produces seasonal averages
def getAverages(values):
    kaverages = []
    raverages = []
    values = [float(item)for item in values]
    numYrs = (len(values)/12)
    #print values[5],values[17],values[29]
    for i in range(1,numYrs):
        # Get SPEI average for kharif season June(6)-October(10)
        k = (i*12)-7
        kaverages.append(np.mean(values[k:(k+5)]))
        #Get SPEI average for Rabi: November(11)-March(3)
        r=(i*12)-2
        raverages.append(np.mean(values[r:(r+5)]))
    averages = [kaverages,raverages]
    return averages


with open('SPEI-test-time.csv', 'rb') as csvfile:
    with open('SPEI-seasonal-avg.csv','wb') as f:
        writer = csv.writer(f,delimiter=',')
        reader = csv.reader(csvfile, delimiter=',')
        header=['Latitude','Longitude','Year','Kharif','Rhabi']
        writer.writerow(header)
        for row in reader:
            if reader.line_num == 1:
                dates = row[3:]
                headYears = map(lambda d:int(d.split('-')[0]),dates)
                headMonths = map(lambda d:int(d.split('-')[1]),dates)
                years = sorted(list(set(headYears)))
            if reader.line_num > 2000 and reader.line_num < 2006:
                lats.append(float(row[1]))
                lons.append(float(row[2]))
                averages = getAverages(row[3:])
                #writeLine
                for i in range(len(years)):
                    writer.writerow([row[1],row[2],years[i],averages[0][i],averages[1][i]])
                    

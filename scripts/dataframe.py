import numpy as np
import csv

lats = []
lons = []
years = []
months = []
# This function accepts a range of SPEI values and produces seasonal averages
def getAverages(values):
    kaverages = []
    raverages = []
    numYrs = (len(values)/12)-1
    #print values[5],values[17],values[29]
    values = map(lambda v: 0 if v=='' else float(v),values)
    for i in range(1,len(years)):
        # Get SPEI average for kharif season June(6)-October(10)
        k = (i*12)-7
        kharif = values[k:(k+5)]
        #Get SPEI average for Rabi: November(11)-March(3)
        r=(i*12)-2
        rhabi = values[r:(r+5)]
        if sum(values) == 0 or len(rhabi)==0:
            kaverages.append(0)
            raverages.append(0)
        else:
            kaverages.append(sum(kharif)/len(kharif))
            raverages.append(sum(rhabi)/len(rhabi))
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
                months = sorted(list(headMonths))
            if reader.line_num >1:
                lats.append(float(row[1]))
                lons.append(float(row[2]))
                averages = getAverages(row[3:])
                for i in range(len(years)-1):
                    writer.writerow([row[1],row[2],years[i],averages[0][i],averages[1][i]])

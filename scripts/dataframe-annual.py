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
        k = (i*12)
        kharif = values[k:(k+12)]

        if sum(values) == 0 or len(kharif)==0:
            kaverages.append(0)
        else:
            kaverages.append(sum(kharif)/len(kharif))
    return kaverages

with open('SPEI-test-time.csv', 'rb') as csvfile:
    with open('SPEI-annual-avg.csv','wb') as f:
        writer = csv.writer(f,delimiter=',')
        reader = csv.reader(csvfile, delimiter=',')
        header=['Latitude','Longitude','Year','Annual Average']
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
                    writer.writerow([row[1],row[2],years[i],averages[i]])

import arcpy as a
import tkFileDialog, Tkinter, Tkconstants
from dbfpy import dbf
from Tkinter import *
from tkFileDialog import *
import glob
a.env.overwriteOutput = True
a.env.Workspace = "C:\\temp"
from arcpy.sa import *
a.CheckOutExtension("Spatial")
outRas = 'C:\\Users\\AMS\\Desktop\\Climate Data\\Season PDSI\\'
clipPolygon = 'C:\\Users\\AMS\\Desktop\\Research\\Grad\\India\\Maps\\DistPop2011.shp'
cdfFolder = 'C:\\Users\\AMS\\Desktop\\Climate Data\\PDSI NC Files\\'
bandDimension = ""
startMo = 1
yearsTotal = 10
dbfstart = 0
i = 0
endMo = 12
print cdfFolder
decade = int(raw_input("By decade (1) or by bi-decade (2) or by tri-decade (3)"))
myStartMo = int(raw_input("What is the start month?"))
myEndMo = int(raw_input("What is the END month?"))
totalMo = yearsTotal * endMo
cdfList = glob.glob(cdfFolder+'/*.nc')
x = 0
tif_files = []
def buildWhereClause(table, field, value):

	# Add DBMS-specific field delimiters
	fieldDelimited = a.AddFieldDelimiters(table, field)

	# Determine field type
	fieldType = a.ListFields(table, field)[0].type

	# Add single-quotes for string field values
	if str(fieldType) == 'String':
    	value = "'%s'" % value

	# Format WHERE clause
	whereClause = "%s = %s" % (fieldDelimited, value)
	return whereClause
for cdf in cdfList:
	x = x + 1
	nc = cdf
	startYear = int(cdf.split('-')[0][-4:])
	endYear = int(cdf.split('-')[1][:-3])
	while(startYear < endYear + 1):
    	while(i < endMo):
        	print startMo
        	i = i + 1
        	if(startMo >= myStartMo and startMo <= myEndMo):
            	newDate = str(startMo) + "/1/"+str(startYear)
            	date = str(newDate)
            	dimensionValues = ['time',{date}]
            	valueSelectionMethod = "BY_VALUE"
           	 out = outRas + "working_ras\\temp\\" + str(startMo)+"_"+str(startYear)+".tif"
            	out2 = outRas + "working_ras\\" + str(startMo)+"_"+str(startYear)+".tif"
            	clip = outRas + "working_ras\\clip\\" +str(startMo)+"_"+str(startYear)+".tif"
            	a.MakeNetCDFRasterLayer_md(nc, 'pdsi','lon','lat',out,'','time '+date,'BY_VALUE')
            	clip = ExtractByMask(out,clipPolygon)
                #a.Clip_management(out,"#",clip,clipPolygon,"#","ClippingGeometry")
                a.CopyRaster_management(clip,out2,"","","","NONE","NONE","")
            	print "Created layer for " + date + " successfully"
            	tif_files.append(out2)
            	startMo = startMo + 1
        	else:
            	startMo = startMo + 1
    	startMo = 1
    	i = 0
    	startYear = startYear + 1
	if(x == decade):
    	if(decade == 1):
        	totaldb = outRas+"Total1.dbf"
    	else:
        	totaldb = outRas+"Total3.dbf"
    	newField = "Mean_"+str(endYear)
    	if(dbfstart == 0):
            #a.AddField_management(totaldb,"State_Dist",'TEXT')
        	newdb = dbf.Dbf(totaldb,new=True)
        	newdb.addField(
                ("State_Dist","C",250),
            	)
        	newdb.close()
            a.AddField_management(totaldb,newField,'FLOAT')
    	else:
            a.AddField_management(totaldb,newField,'FLOAT')
    	x = 0
    	print tif_files
    	y = 0
    	for tif in tif_files:
        	y = y + 1
        	if(y == 1):
            	outrastemp = a.Raster(str(tif))
        	else:
            	listras = a.Raster(str(tif))
            	outrastemp += listras
    	finalras = outrastemp/(len(tif_files))
    	zoneField = "State_Dist"
        outTable = outRas+str(myStartMo)+"_"+str(myEndMo)+"_"+str(endYear)+".dbf"
    	print "Creating table"
    	outZonal = ZonalStatisticsAsTable(clipPolygon,zoneField,finalras,outTable,"NODATA","MEAN")
    	print "Saving decadal pdsi"
    	print totaldb
    	mydb = dbf.Dbf(totaldb)
    	if(dbfstart == 0):
        	db = dbf.Dbf(outTable)
        	dbfstart = 1
        	for rec in db:
            	newrec = mydb.newRecord()
            	newrec["State_Dist"] = rec['State_Dist']
            	newrec.store()
        	db.close()
    	mydb.close()
    	#db = dbf.Dbf(outTable)
    	fieldName = ["State_Dist","MEAN"]
    	db = a.da.SearchCursor(outTable,fieldName)
    	for rec in db:
        	fields = ["State_Dist",newField]
        	cursor = a.da.UpdateCursor(totaldb, fields)
        	#cursor = a.da.UpdateCursor(totaldb,("State_Dist",newField),whereClause)
        	for row in cursor:
            	#print row[0], row[1]
                if(rec[0] == row[0]):
                	#print "FOUND ONE"
                	row[1] = float(rec[1])
                    #row[1].setValue(newField,float(rec['MEAN']))
                	cursor.updateRow(row)
    	dbfstart += 1
   	 savename = outRas+str(myStartMo)+"_"+str(myEndMo)+"_"+str(endYear)+".tif"
    	finalras.save(savename)
    	tif_files = []
print "Done!"

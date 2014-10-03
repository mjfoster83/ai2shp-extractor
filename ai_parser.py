# Michael Foster
# GIS 5562 - Analytical Cartography
# Project
# December 17, 2009
# 
# AItoShapefile.py
#
# Using the existing AI map file "LakeCalhoun.ai", this script loops through and extracts points
# from the AI Postscript file, setting the UTM easting and northing according to the scale, and
# creates a properly projected shapefile containing the linework from the AI file.
#
# NOTE: Requires ArcInfo, works best with AI files backsaved to AI 3.0

# import modules, set up script
import sys, os, string, arcgisscripting
gp = arcgisscripting.create()
gp.overwriteoutput = 1
gp.setProduct("ArcInfo")
gp.addToolbox("C:/arcgis/arcexe9x/Toolboxes/Coverage Tools.tbx")

# set working directory
workspace = "E:/5562Project/fosterProject/"
gp.workspace = workspace

# SET CONSTANTS

# working at scale 1:12,058
# 1 postscript point = 4.2555 meters
# Projection used in Illustrator file is UTM Zone 15N

    # data frame origin
EOrigin = 474068.145225598
NOrigin = 4975089.10248144
    # conversion factor
Conversion = 4.2555
    # projection information
coordsys = "PROJCS['NAD_1983_UTM_Zone_15N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-93.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"

# open ai file to read from and text file to write to
f = open("Lake Calhoun.ai", "r")
g = open("temp.txt", "w")

# for loop through file to pull out points and necessary operators from ai file
# comma separate coordinates and write to a text file.
#
# write to array, append to array

for line in f:
    if line.find("%") != -1:
        print "File scanning... comment deleted"
    else:
        if line.find("m") != -1:
            l = str.split(line)
            n = len(l)
            if n == 3:
                g.write(str((float(l[0])*Conversion)+ EOrigin) + ", " + str((float(l[1])*Conversion)+ NOrigin) + "\n")
                
            elif n == 2:
                g.write(l[0] + "\n")
                
            elif n == 1:
                g.write(l[0] + "\n")
                
        elif line.find("l") != -1:
            l = str.split(line)
            n = len(l)
            if n == 3:
                g.write(str((float(l[0])*Conversion)+ EOrigin) + ", " + str((float(l[1])*Conversion)+ NOrigin) + "\n")
                
            elif n == 2:
                g.write(l[0] + "\n")
                
            elif n == 1:
                g.write(l[0] + "\n")

        elif line.find("S") != -1:
            l = str.split(line)
            n = len(l)
            if n == 3:
                g.write(str((float(l[0])*Conversion)+ EOrigin) + ", " + str((float(l[1])*Conversion)+ NOrigin) + "\n")
                
            elif n == 2:
                g.write(l[0] + "\n")
                
            elif n == 1:
                g.write(l[0] + "\n")

        elif line.find("L") != -1:
            l = str.split(line)
            n = len(l)
            if n == 3:
                g.write(str((float(l[0])*Conversion)+ EOrigin) + ", " + str((float(l[1])*Conversion)+ NOrigin) + "\n")
                
            elif n == 2:
                g.write(l[0] + "\n")
                
            elif n == 1:
                g.write(l[0] + "\n")

        elif line.find("b") != -1:
            l = str.split(line)
            n = len(l)
            if n == 3:
                g.write(str((float(l[0])*Conversion)+ EOrigin) + ", " + str((float(l[1])*Conversion)+ NOrigin) + "\n")
                
            elif n == 2:
                g.write(l[0] + "\n")
                
            elif n == 1:
                g.write(l[0] + "\n")

# close illustrator file because it is no longer needed
f.close()

# close text file to save extracted points and elements
g.close()

# create two new files, one to hold lines and one to hold polygons
a = open("tempLine.txt", "w")
b = open("tempPoly.txt", "w")

# iterate through saved file, writing comma separated points to either of
# two files according to the operator
c = open("temp.txt", "r")

# create empty array to temporarily store read lines
l = []
lineID = 1
polyID = 1
a.write(str(lineID) + "\n")
b.write(str(polyID) + "\n")

for line in c:
    l.append(line)
    
    if line.find("S") != -1:
        l.pop()
        a.writelines(l)
        del l[:]
        lineID = lineID + 1
        a.write("END" + "\n")
        a.write(str(lineID) + "\n")
        print "Polyline written to file."
        
    elif line.find("b") != -1:
        l.pop()
        b.writelines(l)
        del l[:]
        polyID = polyID + 1
        b.write("END" + "\n")
        b.write(str(polyID) + "\n")
        print "Polygon written to file."

# close files to save written coordinates
a.close()
b.close()
c.close()

# open tempLine file and add end to last line to signal end of generate file
a = open ("tempLine.txt","r" )
b = open("line.txt", "w")

l = []

for line in a:
    l.append(line)

l[-1] = "END\n"
b.writelines(l)

a.close()
b.close()


# open tempPoly file and add end to last line to signal end of generate file
a = open ("tempPoly.txt","r" )
b = open("poly.txt", "w")

l = []

for line in a:
    l.append(line)

l[-1] = "END\n"
b.writelines(l)

a.close()
b.close()

# delete temporary files
os.remove("temp.txt")
os.remove("tempPoly.txt")
os.remove("tempLine.txt")

# create new file

# run the generate command to create polyline file
input_line = "line.txt"
output_line = "polylines"

print "Creating polyline coverage for lines..."
gp.Generate_arc(input_line, output_line, "lines")
arc = output_line + "\\arc"
print gp.GetMessages()
gp.refreshCatalog(workspace)

# GENERATE COMMAND FOR POLYGONS WILL GO HERE

# convert coverage to shapefile
print "Creating shapefile from coverage..."
cov = workspace + "shapefiles"
gp.FeatureClassToShapefile_conversion (arc, cov)
print gp.GetMessages()

# define projection of shapefile
print "Defining projection..."
shp = workspace + "shapefiles/polylines_arc.shp"
gp.DefineProjection_management (shp, coordsys)
print gp.GetMessages()

# CREATE POLYGON SHAPEFILES HERE
# DEFINE POLYGON SHAPEFILE PROJECTION HERE

# final status report
print str(lineID - 1) + " polylines extracted from AI file."
print str(polyID - 1) + " polygons extracted from AI file."
print "AI to Shapefile completed."

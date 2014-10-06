# ai_parser.py
#
# =============================================================================================
#
# Author: Michael Foster
# October 2, 2014
#
# Using the existing AI map file "LakeCalhoun.ai", this script loops through and extracts points
# from the AI Postscript file, setting the UTM easting and northing according to the scale, and
# creates a properly projected shapefile containing the linework from the AI file.
#
# NOTE: Requires ArcInfo, works best with AI files backsaved to AI 3.0

# import modules, set up script
import sys, os, string, csv
import arcpy
from arcpy import env

# set workspace
env.workspace = "C:/Users/Mike/Documents/GitHub/ai-parser"

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
coordsys = r"Coordinate Systems\Projected Coordinate Systems\Utm\Nad 1983\NAD 1983 UTM Zone 15N.prj"

# open ai file to read from and text file to write to
f = open("LakeCalhoun.ai", "r")
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
allID = 1
lineID = 1
polyID = 1
drawOrder = 1
a.write(str("LINEID,DRAWORD,POINT_X,POINT_Y") + "\n")
b.write(str("POLYID,DRAWORD,POINT_X,POINT_Y") + "\n")

for line in c:
    l.append(str(allID)+str(", ")+str(drawOrder)+str(", ")+line)
    drawOrder = drawOrder + 1
    
    if line.find("S") != -1:
        l.pop()
        a.writelines(l)
        del l[:]
        lineID = lineID + 1
        allID = allID + 1
        # a.write("END" + "\n")
        # a.write(str(lineID) + "\n")
        print "Polyline written to file."
        
    elif line.find("b") != -1:
        l.pop()
        b.writelines(l)
        del l[:]
        polyID = polyID + 1
        allID = allID + 1
        # b.write("END" + "\n")
        # b.write(str(polyID) + "\n")
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

b.writelines(l)

a.close()
b.close()


# open tempPoly file and add end to last line to signal end of generate file
a = open ("tempPoly.txt","r" )
b = open("poly.txt", "w")

l = []

for line in a:
    l.append(line)

b.writelines(l)

a.close()
b.close()

# delete temporary files
os.remove("temp.txt")
os.remove("tempPoly.txt")
os.remove("tempLine.txt")

# GENERATE NEW POLYLINE SHAPEFILE
# create a Polyline XY Event Layer
print "Creating polyline event layer for lines..."
try:
    # Set the local variables
    in_Table = "line.txt"
    x_coords = "POINT_X"
    y_coords = "POINT_Y"
    out_Layer = "convert_lines"
    saved_Layer = "lines.lyr"
 
    # Set the spatial reference
    spRef = coordsys
 
    # Make the XY event layer...
    arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef)
 
    # Print the total rows
    print arcpy.GetCount_management(out_Layer)
 
    # Save to a layer file
    arcpy.SaveToLayerFile_management(out_Layer, saved_Layer)
 
except:
    # If an error occurred print the message to the screen
    print arcpy.GetMessages()

# Create point shapefile from Polyline XY Layer
# Set local variables
inFeatures = ["lines.lyr"]
outLocation = "/temp/"
 
# Execute FeatureClassToGeodatabase
arcpy.FeatureClassToShapefile_conversion(inFeatures, outLocation)

# Create Line Shapefile
# Set local variables
inFeatures = "/temp/convert_lines.shp"
outFeatures = "/final_output/lines.shp"
lineField = "LINEID"
sortField = "DRAWORD"

# Execute PointsToLine on Convert Lines File
arcpy.PointsToLine_management(inFeatures, outFeatures, lineField, sortField)

# Delete Convert Lines File
arcpy.Delete_management("/temp/convert_lines.shp", "")

# GENERATE NEW POLYGON SHAPEFILE
# create a Polyline XY Event Layer
print "Creating polygon event layer for lines..."
try:
    # Set the local variables
    in_Table = "poly.txt"
    x_coords = "POINT_X"
    y_coords = "POINT_Y"
    out_Layer = "convert_poly"
    saved_Layer = "poly.lyr"
 
    # Set the spatial reference
    spRef = coordsys
 
    # Make the XY event layer...
    arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef)
 
    # Print the total rows
    print arcpy.GetCount_management(out_Layer)
 
    # Save to a layer file
    arcpy.SaveToLayerFile_management(out_Layer, saved_Layer)
 
except:
    # If an error occurred print the message to the screen
    print arcpy.GetMessages()

# Create point shapefile from Polyline XY Layer
# Set local variables
inFeatures = ["poly.lyr"]
outLocation = "/temp/"
 
# Execute FeatureClassToGeodatabase
arcpy.FeatureClassToShapefile_conversion(inFeatures, outLocation)

# Create Line Shapefile
# Set local variables
inFeatures = "/temp/convert_poly.shp"
outFeatures = "/temp/convert_featurepoly.shp"
lineField = "POLYID"
sortField = "DRAWORD"

# Execute PointsToLine on Convert Lines File
arcpy.PointsToLine_management(inFeatures, outFeatures, lineField, sortField)

# Delete Convert Lines File
arcpy.Delete_management("/temp/convert_poly.shp", "")

# Create Polygon File from Line file
# Set local parameters
inFeatures = "/temp/convert_featurepoly.shp"
outFeatureClass = "/final_output/poly.shp"
clusTol = "0.05 Meters"

# Use the FeatureToPolygon function to form new areas
arcpy.FeatureToPolygon_management(inFeatures, outFeatureClass, clusTol, "NO_ATTRIBUTES", "")

# delete temporary files
os.remove("line.txt")
os.remove("poly.txt")

# Delete Unused Layer File
arcpy.Delete_management("poly.lyr", "")
arcpy.Delete_management("lines.lyr", "")

# final status report
print str(lineID - 1) + " polylines extracted from AI file."
print str(polyID - 1) + " polygons extracted from AI file."
print "AI to Shapefile completed."

#------------------------------
# Author: Chris Stayte
# Team: Remote Sensing
# Date: Febuary 10, 2017
# Attempt to find coordinates of search names from a comma delimited csv file
#------------------------------

import csv
from geopy.geocoders import Nominatim
import os
import time

print ("Input:  Comma Delimited List With Location Names" + 
    "\nOutput: Comma Delimited List With Location Names and Coordinates")

input_file_path = input("CSV Input File Path: ")
#input_file_path = r"C:\Users\Stayte\Desktop\Canadian_Cities.csv"

print ('\n\nSTART ' + time.ctime())
start_time = time.time()

if not os.path.exists(input_file_path):
    print("\n\nFile Doesn't Exist")
    input("press enter to exit")
    sys.exit()

row_count = 0
search_array = {}

with open(input_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=",", quotechar="\"")
    for row in reader:
        row_count += 1
        try:
            item_list = []
            for item in row:
                item_list.append(item)
            search_array[row_count] = item_list

        except Exception as e:
            print("\n\nError On Row: " + row_count + "\nError Message: " + e)

(filepath, filename) = os.path.split(input_file_path)
(shortname, extension) = os.path.splitext(filename)

output_file_path = filepath + "\\" + shortname + "_Results.csv"

print ("\n\nProcessing " + str(row_count) + " Locations\n")

with open(output_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=",", quotechar="\"")
    writer.writerow(["Search Name", "Longitude", "Latitude"])

    geolocator = Nominatim()

    for index in search_array:

        search_string = ""
        for item in search_array[index]:
            search_string += (item + " ")
            
        try:
            location = geolocator.geocode(search_string)
        except Exception:
            location = None
        latitude = "None"
        longitude = "None"
        
        if location != None:
            latitude = str(location.latitude)
            longitude = str(location.longitude)

        
        writer.writerow([search_string, longitude, latitude])
        
        percent_complete = round((index / row_count) * 100, 2)
        print(str(percent_complete) + "% Complete")


print ('\n\nEND ' + time.ctime())
seconds = time.time() - start_time
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
print ("Time elapsed: " + "%d:%02d:%02d" % (h, m, s))
input("\npress enter to exit")

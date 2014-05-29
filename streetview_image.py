import argparse
import os
import random
import sys
import urllib
from math import radians, cos, sin, asin, sqrt
import math

# Google Street View Image
# 25,000 image requests per 24 hours
# See https://developers.google.com/maps/documentation/streetview/
API_KEY = "INSERT_YOUR_API_KEY_HERE"
GOOGLE_URL = "http://maps.googleapis.com/maps/api/streetview?sensor=false&size=640x640"
#GOOGLE_URL = "http://maps.googleapis.com/maps/api/streetview?sensor=false&size=640x640" + API_KEY #Uncomment this line if you have a Google API Key



def main():
	gps = open(sys.argv[1], 'r')
	gpsdata = [line.split(';') for line in gps]
	run(gpsdata)
		
def run(gpsdata):
	count = 0
	curr = (gpsdata[0][1], gpsdata[0][2])
	for entry in gpsdata:
		dist = haversine(curr[0], curr[1], entry[1], entry[2])
		if dist > 10: #grab image in a distance interval
			count = count + 1
			heading = direction(curr[0], curr[1], entry[1], entry[2]) #Compute current heading
			curr = (entry[1], entry[2])
		#	print '[' + str(count)+'] distance: ' + str(dist) + ' heading: ' + str(heading)
			getImage(entry[1],entry[2], 'img'+str(count), heading)
		if count > 20:
			break
	
def direction(lon1, lat1, lon2, lat2):
	"""
	Calculate current heading of the camera based on two GPS locations
	"""
	hor = float(lon2)-float(lon1)
	ver = float(lat2)-float(lat1)	
	angle = math.degrees(math.atan2(hor,ver))
	angle = angle if angle > 0 else 180-angle	

	return angle		

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    m = 6367 * c * 1000
    return m



def getImage(lon, lat, fname, heading):
	print "Getting " + fname
	lat_lon = lon + ',' + lat
	#dir_l = heading-45 if heading-45>=0 else heading-45+360
	#dir_r = heading+45 if heading+45<=360 else heading+45-360
	dir_l = heading-90 if heading-90>=0 else heading-90+360
	dir_r = heading

	url = GOOGLE_URL + "&location=" + lat_lon
	url_l = url + "&heading="+str(dir_l)
	url_r = url + "&heading="+str(dir_r)
	try:
		urllib.urlretrieve(url_l, 'imgs/' + fname+'_l.jpg')
		urllib.urlretrieve(url_r, 'imgs/' + fname+'_r.jpg')
	except:
		pass


	
if __name__=="__main__":
	main()


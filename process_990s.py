#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 13:08:23 2019

@author: egavis
"""

import os

#import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(user_agent="my-application", format_string="%s, Chicago IL")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

###COORDINATES FOR THE 5 COMMUNITY AREAS 
def id_community():
    return ""

#GEOPY THE ADDRESS
def determine_coordinates(street):
    #street = "1005 E 60th Street"
    address, (latitude, longitude) = geocode(street)
    #print(address)
    return latitude, longitude

def list_990s():
    return sorted(os.listdir("form_990s/forms"))

for fname in list_990s():
    break
        

#WRITE A TEXT FILE OF THE ONES THAT ARE

#USE THOSE FOR LATER ANALYSIS/STORAGE
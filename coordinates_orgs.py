#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 14:18:12 2019

@author: jgavis
"""
#10964
import time
import csv
import re
import progressbar
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(user_agent="my-gis-application", format_string="%s, Chicago IL")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=10, 
                      error_wait_seconds=10.0)

def previously_done():
    with open("orgs_lat_long.csv") as f:
        spamreader = csv.reader(f)
        next(spamreader)
        rv = []
        for row in spamreader:
            if row[5] != "error":
                rv.append(row[0])
        return set(rv)
                
#GEOPY THE ADDRESS
def determine_coordinates(street):
    #street = "1005 E 60th Street"
    try:
        address, (latitude, longitude) = geocode(street)
    except:
        latitude = "error"
        longitude = "error"
    return latitude, longitude

def fix_street(street):
    return re.sub(r"STE .*|APT .*|FL .*|IL[0-9I]-.*|" 
                    r"[0-9 ]+[TH]* FL.*|RM .*|UNIT .*| NO .*|"
                    r"UNT .*|SUITE .*|DIV .*|-[0-9]+|#.*|NUM .*|"
                    r"APARTMENT .*|FLOOR .*|[0-9][A-Z] .*",
                        "", street).strip()

def main():
    bar = progressbar.ProgressBar(max_value=19807)
    done = previously_done()
    with open("orgs_lat_long_2.csv", "w") as f1:
        spamwriter = csv.writer(f1)
        with open("orgs_addresses.csv", "r") as f2:  
            org_reader = csv.reader(f2)
            spamwriter.writerow(next(org_reader) + ["lat", "lon"])
            c = 0
            for row in org_reader:
                c += 1
                bar.update(c)
                if row[0] in done or "PO BOX" in row[1] or len(row[1]) < 5:
                    continue
                lat, lon = determine_coordinates(fix_street(row[1]))
                spamwriter.writerow(row + [lat, lon])
                
if __name__ == "__main__":
    main()

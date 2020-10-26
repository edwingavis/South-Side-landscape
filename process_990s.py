#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 13:08:23 2019

@author: jgavis
"""

import os
import json
import csv

#import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(user_agent="my-application", format_string="%s, Chicago IL")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

###COORDINATES FOR THE 5 COMMUNITY AREAS 
def id_community():
    '''
    '''
    return

#GEOPY THE ADDRESS
def determine_coordinates(street):
    #street = "1005 E 60th Street"
    address, (latitude, longitude) = geocode(street)
    #print(address)
    return latitude, longitude

def list_990s():
    return sorted(os.listdir("form_990s/forms"))
    
def process_990s():
    '''
    '''
    for fname in list_990s():
        with open("form_990s/forms/" + fname) as f:
            j = json.load(f)
        yield j
        #print(json.dumps(j, indent=4))

def generate_rows():
    cols = False
    for j in process_990s():
        if not cols:
            org_col = sorted(j["organization"].keys())
            forms_col = sorted(j["filings_with_data"][0].keys())        
            cols = True
            yield org_col, [forms_col]
        org = [e[1] for e in sorted(j["organization"].items())]
        forms = []
        for f in (j["filings_with_data"] + j["filings_without_data"]):
            form = []
            for col in forms_col:
                try:
                    form.append(f[col])
                except KeyError:
                    if col == "ein":
                        form.append(j["organization"]["ein"])
                    else:
                        form.append("")
            forms.append(form)
        yield org, forms
    
def write_to_csv():
    with open("orgs.csv", "w") as f, open("forms.csv", "w") as g:
        f_writer = csv.writer(f, delimiter='|', 
                              quotechar='"', quoting=csv.QUOTE_MINIMAL)
        g_writer = csv.writer(g, delimiter='|', 
                              quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for org, forms in generate_rows():
            f_writer.writerow(org)
            for form in forms:
                g_writer.writerow(form)
            #return #DEBUGGING

if __name__ == "__main__":
    #write_to_csv() # for creating initial csvs
    pass

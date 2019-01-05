#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 11:32:50 2019

@author: egavis
"""

import json
import urllib3
import time
import os

import progressbar

SLEEP_TIME = 2

http = urllib3.PoolManager()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

pp_api = "https://projects.propublica.org/nonprofits/api/v2/"

def get_search_results():
    '''
    '''
    with open("chicago.json") as f:
        initial = json.load(f)
        pages = initial["num_pages"]
        digits = len(str(pages))
    for p in progressbar.progressbar(range(pages)):
        url = pp_api + "search.json?q=chicago&page="
        j = http.request('GET', url + str(p)).data
        fname = "chicago_" + make_length(str(p), digits) 
        with open("form_990s/results/" + fname, "w") as f:
            json.dump(json.loads(j.decode('utf-8')), f)
        time.sleep(SLEEP_TIME) #being nice to PP

def make_length(p, digits):
    '''
    '''
    while len(p) < digits:
        p = "0" + p
    return p

def get_990s():
    '''
    '''
    folder = "form_990s/results/"
    files = os.listdir(folder) #sort
    #files = files[187:] #comment out
    for search in progressbar.progressbar(files):
        with open("%s/%s" % (folder,search)) as f:
            j = json.load(f)
        for org in j["organizations"]:
            ein = org["ein"]
            url = pp_api + "organizations/%d.json" % ein
            #print(url)
            filing = http.request('GET', url).data
            with open("form_990s/forms/" + str(ein), "w") as f:
                json.dump(json.loads(filing.decode('utf-8')), f)
            time.sleep(SLEEP_TIME) #being nice to PP

if __name__ == "__main__":
    get_search_results()
    get_990s()
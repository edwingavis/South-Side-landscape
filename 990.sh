#!/bin/bash
# My first script
curl -o chicago.json https://projects.propublica.org/nonprofits/api/v2/search.json?q=chicago
mkdir form990s
mkdir form990s/results
mkdir form990s/forms

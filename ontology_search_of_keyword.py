import urllib.request, urllib.error, urllib.parse
import json
import os, re
from pprint import pprint

REST_URL = "http://data.bioontology.org"
API_KEY = " "

def get_json(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
    return json.loads(opener.open(url).read())

with open("./BrainRegions.csv") as f:
    content = f.readlines()

Acronyms=[]
for line in content:
    terms = re.split(" ?; ?| ?, ?", line.strip().lower())  # Split terms
    terms = filter(bool, terms)  # Remove empty values
    terms = list(terms)
    Acronyms+=terms

keywords=set(Acronyms)
count=0
params=[]
for trm in keywords:
    if count!=500:
        if(" " in trm):
            trm=urllib.parse.quote(trm)
        params.append(trm)
        count+=len(trm)
    if count >= 500:
        break

ontology_output = []
# Do a search for every term
for term in params:
    search_results = []
    search_results.append(get_json(REST_URL + "/search?q=" + term)["collection"])
    ontologies=set()
    for i in range(0, len(search_results[0])):
        ontology=re.split('\\b/\\b',search_results[0][i]['links']['ontology'])[-1]
        ontologies.add(ontology)

    ontology_output.append(term+" => "+str(ontologies))

# Print the results
f = open("index.txt", "w")
for out in ontology_output:
    f.write(out+ '\n')
#pprint(ontology_output)


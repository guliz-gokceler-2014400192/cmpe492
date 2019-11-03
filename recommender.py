import urllib.request, urllib.error, urllib.parse
import json
import os, re
from pprint import pprint

REST_URL="http://data.bioontology.org"
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

f = open("index.txt", "w")
keywords=set(Acronyms)
count=0
word_count=0
params=""
controlled=set()
for trm in keywords:
    if count!=7500:
        if(" " in trm):
            trm=urllib.parse.quote(trm)
        f.write(trm+",")
        params+=trm
        params+=","
    else:
        f.write(trm)
        params+=trm
    controlled.add(trm)
    count+=len(trm)
    word_count+=1
    if count>=7500:
        print(trm)
        break
#f.close()

search_results = []
search_results.append(get_json(REST_URL + "/recommender?input=" + params + "&input_type=2"))



print("\n\n")
count=0
for ont in search_results:
    for count in range(0,len(ont)):
        print("{} with score {}".format(ont[count]['ontologies'][0]['acronym'], ont[count]['evaluationScore']))
        print("\n")
        count=count+1
    
print("\n\n")
count=0
matches=[]
for ont in search_results:
    for count in range(0,len(ont)):
        for count2 in range(0,len(ont[count]['coverageResult']['annotations'])):
            matches.append(ont[count]['coverageResult']['annotations'][count2]['text'])
            count2=count2+1
        count=count+1
matched=set(matches)    
print(len(keywords))
print(word_count)
print(len(matched))
d1 = {v.lower(): v for v in controlled}
d2 = {v.lower(): v for v in matched}

k1 = set(d1.keys())
k2 = set(d2.keys())
a=k1.difference(k2)


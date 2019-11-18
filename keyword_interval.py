import urllib.request, urllib.error, urllib.parse
import json
import os, re
from pprint import pprint
from nltk.tokenize import sent_tokenize, word_tokenize

REST_URL="http://data.bioontology.org"
API_KEY = "6d83328b-ba5a-47da-b51e-43ae69b9bc66"

def findall(p, s):
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)


def get_json(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
    return json.loads(opener.open(url).read())

def keyword_interval(flag):
    keyword=["aMygdala", "amygdalae", "amygdalar"]
    [x.lower() for x in keyword]
    title_or_abstract=flag #0 means title, 1 means abstract
    synonyms=[]
    synonyms+=keyword
    for term in keyword:
        data=get_json(REST_URL + "/search?q="+ term+"&ontologies=NIFSTD")['collection']
        for i in range(0,len(data)):
            if 'synonym' in data[i]:
                synonyms+=(data[i]['synonym'])

    synonyms=[x.lower() for x in synonyms]
    synonyms={*synonyms}
    start_end_points=[]
    if title_or_abstract==0:
        with open('article.json') as json_file:
            data = json.load(json_file)
            title=data['title'].lower()
            #print(title)

        for syn in synonyms:
            if syn in title:
                start_end_points+=[(i, i+len(syn)-1, title[i:i+len(syn)]) for i in findall(syn, title)]

    else:
        with open('article.json') as json_file:
            data = json.load(json_file)
            abstract=data['abstract'].lower()
        id=0
        sentences=sent_tokenize(abstract)
        sentence_dict=dict()
        for sentence in sentences:
            sentence_dict[id]=sentence
            id+=1
        #print(sentence_dict)

        for syn in synonyms:
            for id in sentence_dict:
                sent=sentence_dict[id]
                if syn in sent:
                    start_end_points+=[("sent id: "+str(id),i, i+len(syn)-1) for i in findall(syn, sent)]
    print(start_end_points)
    print(synonyms)

title_or_abstract=0
keyword_interval(title_or_abstract)
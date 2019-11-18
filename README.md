# cmpe492

Run with "python3 <file_name>
* recommender.py is to get recommended ontology for a given set of keywords in "BrainRegions.csv". Number of characters to be sent as request is limited to 500 words. 
* ontology_search_for_keyword.py is to get ontologies corresponding a keyword. Slow search! It outputs the keywords with their ontologies into index.txt file. 
* keyword_interval.py is to get positions of keyword(s) and its(their) synonyms taken from NIFSTD ontology in a given article. Looks for title and abstract of the article. Tokenizes the abstract to its sentences and after search of the terms, identifies their position in each sentence.  

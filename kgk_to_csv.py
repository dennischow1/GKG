#!/usr/bin/env python
"""
Query the Knowledge Graph API https://developers.google.com/knowledge-graph/
"""

#import argparse
import datetime
#import requests
import json
import urllib.parse
import urllib.request
import csv

def query_KG(query):
    """
    Query the Knowledge Graph API https://developers.goog.com/knowledge-graph/
    """
    api_key = open('api_key.txt').read()
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'

    params = {
        'query': query,
        'limit': 100,
        'indent': True,
        'key': api_key,
        }
    url = service_url + '?' + urllib.parse.urlencode(params)  # TODO: use requests
    response = json.loads(urllib.request.urlopen(url).read())
    return response

def add_to_csv(item,query,fieldnames):
    """
    Adds item into CSV file
    """
    try:
        name = str(item['result']['name'])
    except KeyError:
        name = "N/A"

    try:
        entity_type = str(", ".join([n for n in item['result']['@type']]))
    except KeyError:
        entity_type = "N/A"
    
    try:
        desc = str(item['result']['description'])
    except KeyError:
        desc = "N/A"

    try:
        detail_desc = str(repr(item['result']['detailedDescription']['articleBody']))
    except KeyError:
        detail_desc = "N/A"

    try:
        score = str(item['resultScore'])
    except KeyError:
        score = "N/A"

    rowDict = {'query_term':query,'name':name,'entity_type':entity_type,'description':desc,'detailed_description':detail_desc,'resultScore':score}
    
    with open('training_set.csv',mode='a', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow(rowDict)

if __name__ == '__main__':

    text_file = open("words.txt","r")
    words = text_file.read().split(',')
    
    #TODO create gas station related dictionary
    with open('training_set.csv',mode='w', encoding='utf-8') as csv_file:
        fieldnames = ['query_term','name','entity_type','description','detailed_description', 'resultScore']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

    for query in words:
        response = query_KG(query)
        for item in response['itemListElement']:
            add_to_csv(item,query,fieldnames)

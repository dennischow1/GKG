import argparse
import datetime
#import requests
import json
import urllib.parse, urllib.request
from py2neo import Graph, Node, Relationship


def query_KG(query):
    """
    Query the Knowledge Graph API https://developers.goog.com/knowledge-graph/
    """
    api_key = open('api_key.txt').read()
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'

    params = {
        'query': query,
        'limit': 5,
        'indent': True,
        'key': api_key,
        }

    url = service_url + '?' + urllib.parse.urlencode(params)  # TODO: use requests
    response = json.loads(urllib.request.urlopen(url).read())

    return response
  
def upload_entity(entry):
    """
    Upload entry into Graph database
    """
    
    graph = Graph('http://localhost:7474/db/data/',
                  user=open('neo4j_user.txt').read(),
                  password = open('neo4j_pass.txt').read())

    id_num = entry['result']['@id']
    name = entry['result']['name']
    description = entry['result']['description']
    entity = Node('Entity', id=id_num, description=description,name=name)
    graph.merge(entity, 'Entity', 'id')
    graph.merge(entity, 'Entity', 'description')
    graph.merge(entity, 'Entity', 'name')
    for n in entry['result']['@type']:
        item = Node('Item', type=n)
        graph.merge(item, 'Item', 'type')
        graph.merge(Relationship(entity, "IS", item))

def constraint(label, property):
    graph = Graph('http://localhost:7474/db/data/',
              user=open('neo4j_user.txt').read(),
              password = open('neo4j_pass.txt').read())
    schema = graph.schema
    if property not in schema.get_uniqueness_constraints(label):
        schema.create_uniqueness_constraint(label,property)

if __name__ =='__main__':
    constraint('Entity','id')
    constraint('Item','type')

    response = query_KG('Taylor')
    for entity in response['itemListElement']:
        upload_entity(entity)

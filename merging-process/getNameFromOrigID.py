import csv
import requests

file = csv.reader(open('/Users/faithlawrence/Documents/KCL/SNAP/svn/data/MergeLists/LGPN-PIRmapping.csv', 'r'))

lgpn_prefix = "http://www.lgpn.ox.ac.uk/id/"
pir_prefix = "http://www.paregorios.org/resources/roman-elites/persons/"

for row in file:
    lgpn_id, pir_id = row
    
    sparql_target = 'https://snap.dighum.kcl.ac.uk/sparql/'
    sparql_query_key = 'query'
    query = ''
    query += 'PREFIX foaf:  <http://xmlns.com/foaf/0.1/> SELECT DISTINCT ?name { <' + lgpn_prefix + lgpn_id +'> foaf:name ?name}'
    data = {sparql_query_key: query}
    headers = {'Accept': 'application/sparql-results+json'}
    r = requests.get(sparql_target, params=data, headers=headers, verify=False)
    jsonData = r.json()
    results = jsonData['results']['bindings']

    name=results[0]['name']['value']
    
    print lgpn_id + ': ' + name + "\n"
        
        
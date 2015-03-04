import csv
import requests
import collections
from collections import Counter
from lxml import etree as ET

reader = csv.reader(open('C:\Users\DigiHum\Desktop\SNAP svn\pythonscripts\LGPN-PIRmapping.csv', 'r'))
l_big=[]

prefix1 = "http://www.lgpn.ox.ac.uk/id/"
prefix2 = "http://www.paregorios.org/resources/roman-elites/persons/"

for row in reader:
    l_small=[]
    v1,v2=row
    v1 = prefix1 + v1
    l_small.append(v1)
    v2 = prefix2 + v2
    l_small.append(v2)
    l_big.append(l_small)
#create a list of all the http in the source

def sparqlquery():
    for i in range(len(l_big)): #i is the progressive number of list in list of lists
        httpquery = l_big[i][0] #this is the left-side value
    ##sparqlquery as follows:
        sparql_target = 'https://snap.dighum.kcl.ac.uk/sparql/'
        sparql_query_key = 'query'
        query = ''
        query += 'PREFIX prov: <http://www.w3.org/ns/prov#> SELECT DISTINCT ?id { ?id prov:DerivedFrom <'+ httpquery +'>}'
        data = {sparql_query_key: query}
        headers = {'Accept': 'application/sparql-results+json'}
        r = requests.get(sparql_target, params=data, headers=headers, verify=False)
        jsonData = r.json()
        results = jsonData['results']['bindings']
    ##sparqlquery end
        snapid=results[0]['id']['value']
        l_big[i].append(snapid)

sparqlquery()

snapids = []
for i in range(len(l_big)):
    snapids.append(l_big[i][2])

snapdupls = [x for x,y in collections.Counter(snapids).items() if y>1]

def maketemplate():
    root = ET.Element("root")
    for i in range(len(l_big)):
        snap_id = l_big[i][2]
        lgpn_id = l_big[i][0]
        pir_id = l_big[i][1]
        doc = ET.SubElement(root, "doc")
#field:
        snapid = ET.SubElement(doc, "snapid")
        snapid.text = snap_id
#field:
        type = ET.SubElement(doc, "type")
        type.text = "rdf:type lawd:Person, snap:MergedResource ;"
#field:
        dcreplaces = ET.SubElement(doc, "dcreplaces")
        dcreplaces.text = "dc:replaces " + lgpn_id + " ;"
#field:
        dcreplaces = ET.SubElement(doc, "dcreplaces")
        dcreplaces.text = "dc:replaces " + pir_id + " ;"
#tree
        tree = ET.ElementTree(root)
        tree.write("C:/Users/DigiHum/Desktop/template.xml", pretty_print=True) #always needs slash forward, doesnt understand back slash

maketemplate()

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
    for i in range(0,181):
        httpquery0 = l_big[i][0] #this is the left-side value
        httpquery1 = l_big[i][1] #this is the right-side value
        sparql_target = 'https://snap.dighum.kcl.ac.uk/sparql/'
        sparql_query_key = 'query'
    ##sparqlquery left:
        query0 = ''
        query0 += 'PREFIX prov: <http://www.w3.org/ns/prov#> SELECT DISTINCT ?id { ?id prov:DerivedFrom <'+ httpquery0 +'>}'
        data = {sparql_query_key: query0}
        headers = {'Accept': 'application/sparql-results+json'}
        r0 = requests.get(sparql_target, params=data, headers=headers, verify=False)
        jsonData0 = r0.json()
        results0 = jsonData0['results']['bindings']
        snapid0=results0[0]['id']['value']
    ##sparqlquery right:
        if i == 134 or i == 137 or i == 158 or i == 159 or i == 160 or i == 172:
            l_big[i].append(snapid0)
            l_big[i].append("SNAPID NOT AVAILABLE")
        else:
            query1 = ''
            query1 += 'PREFIX prov: <http://www.w3.org/ns/prov#> SELECT DISTINCT ?id { ?id prov:DerivedFrom <'+ httpquery1 +'>}'
            data = {sparql_query_key: query1}
            headers = {'Accept': 'application/sparql-results+json'}
            r1 = requests.get(sparql_target, params=data, headers=headers, verify=False)
            jsonData1 = r1.json()
            results1 = jsonData1['results']['bindings']
            snapid1=results1[0]['id']['value'] #this line generated the IndexError:list index out of range
            l_big[i].append(snapid0)
            l_big[i].append(snapid1)

sparqlquery()

def maketemplate():
    file = open("C:/Users/DigiHum/Desktop/SNAP svn/pythonscripts/template1.rdf", "w")
    file.write("@prefix: <http://onto.snapdrgn.net/snap#> .\n@prefix dc: <http://purl.org/dc/elements/1.1/> .\n@prefix snap: <http://onto.snapdrgn.net/snap#> .\n@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n@prefix lawd: <http://lawd.info/ontology/> .\n")
    for i in range(0,181):
        newid=673754+i
        new_snap_id="http://data.snapdrgn.net/person/"+str(newid)+"/"        
        old_snap_id0 = l_big[i][2]
        old_snap_id1 = l_big[i][3]
        file.write("\n<" + new_snap_id + ">")
        file.write("\na lawd:Person, snap:MergedResource ;")
        file.write("\ndc:replaces <" + old_snap_id0 + "> ;")
        file.write("\ndc:replaces <" + old_snap_id1 + "> ;")
        file.write("\ndc:publisher <???> .\n")
    file.close()

maketemplate()

#to check dupls:
snapids = []
for i in range(len(l_big)):
    snapids.append(l_big[i][2])

snapdupls = [x for x,y in collections.Counter(snapids).items() if y>1]
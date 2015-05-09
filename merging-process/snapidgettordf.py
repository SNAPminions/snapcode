import csv
import requests
#import collections
#import simplejson as json
#from collections import Counter
#from lxml import etree


#ToDo:
#write the Double-ID check
# get rid of "i"
# solve the "exception"-problem (if i == 134 or i == 137 or i == 158 or i == 159 or i == 160 or i == 172:)
# create the parameter inside the request.

#what ist the output of "reader"? tuples? or lists?


reader = csv.reader(open('/Users/MHuber/Documents/snap/snapcode/merging-process/data/LGPN-PIRmapping.csv', 'r'))
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
    #l_big looks like [[prefix1+row1,prefix2+row1][prefix1+row2, prefix2+row2]...]
#create a list of all the http in the source

def sparqlquery():
    #for index, content in enumerate(l_big):

    for i in range(0,181):
        httpquery0 = l_big[i][0] #this is the left-side value
        httpquery1 = l_big[i][1] #this is the right-side value
        sparql_target = 'https://snap.dighum.kcl.ac.uk/sparql/'
        sparql_query_key = 'query'
    ##sparqlquery left:
        query0 = ''
        query0 += 'PREFIX prov: <http://www.w3.org/ns/prov#> SELECT DISTINCT ?id { ?id prov:wasDerivedFrom <'+ httpquery0 +'>}' #"+=" == "="
        data = {sparql_query_key: query0}
        headers = {'Accept': 'application/sparql-results+json'}
        r0 = requests.get(sparql_target, params=data, headers=headers, verify=False)
        jsonData0 = r0.json()#what does the output look like? (next line) are there alternatives to json?
        print (jsonData0)
        results0 = jsonData0['results']['bindings']
        snapid0=results0[0]['id']['value']
    ##sparqlquery right:
        if i == 134 or i == 137 or i == 158 or i == 159 or i == 160 or i == 172:
            l_big[i].append(snapid0)
            l_big[i].append("SNAPID NOT AVAILABLE")
        else:
            query1 = ''
            query1 += 'PREFIX prov: <http://www.w3.org/ns/prov#> SELECT DISTINCT ?id { ?id prov:wasDerivedFrom <'+ httpquery1 +'>}'
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
    snapfile = open("/Users/MHuber/Documents/snap/snapcode/merging-process/template1.rdf", "w")
    snapfile.write("@prefix: <http://onto.snapdrgn.net/snap#> .\n@prefix dct: <http://purl.org/dc/elements/1.1/> .\n@prefix snap: <http://onto.snapdrgn.net/snap#> .\n@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n@prefix lawd: <http://lawd.info/ontology/> .\n")
    for i in range(0,181):
        newid=673754+i
        new_snap_id="http://data.snapdrgn.net/person/"+str(newid)+"/"
        old_snap_id0 = l_big[i][2] #result1
        old_snap_id1 = l_big[i][3] #result2
        snapfile.write("\n<" + new_snap_id + ">")
        snapfile.write("\na lawd:Person, snap:MergedResource ;")
        snapfile.write("\ndct:replaces <" + old_snap_id0 + "> ;")
        snapfile.write("\ndct:replaces <" + old_snap_id1 + "> ;")
        snapfile.write("\ndct:publisher <???> .\n") #need to be added
    snapfile.close()

maketemplate()

#to check dupls:
#snapids = []

#
#for i in range(len(l_big)):
#    if (l_big[i]>1):
#        snapids.append(l_big[i][2])

#snapdupls = [x for x,y in list(collections.Counter(snapids).items()) if y>1]
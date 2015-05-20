import csv
import requests
import os

#ToDo
#if the person is already merged with a another 'prefix'+id, then add the 'new' id to the already existing dataset
#



##global Variables
#How to get rid of them?
i= 0
tempVar = ''
def consoleInput():
    consoleInputID = raw_input('insert the number where the already existing snap-id count ends; means highest id-value')
    if not consoleInputID.isdigit():
        print('Your input is not a number. please try again')
        consoleInput()

    consoleInputFilePathCSV = raw_input('insert the relative or absolute path to the CSV file')
    if not os.path.isfile(consoleInputFilePathCSV):
        print('Your file does not exist')
        consoleInput()

    consoleOutputFilePathRDF = raw_input('insert directory for the output RDF-file; to create the file at the current directory, insert "."')
    if not os.path.isdir(consoleOutputFilePathRDF):
        print('Your insert directory does not exist')
        consoleInput()
    consoleOutputFilePathRDF = consoleOutputFilePathRDF + '/' + os.path.basename(consoleInputFilePathCSV) + 'mergedTriplets.rdf'

    instantiateTemplate(consoleOutputFilePathRDF)


    mergingCSV(consoleInputFilePathCSV, consoleInputID, consoleOutputFilePathRDF)

##To Do:
#maybe create a file which saves the last snap-id count.

#maybe write an if-clause which checks the absolute number of snap-ids/entries in the database and create a print output if the input number is lower
#or does not continue the current count

#incorporate GUI? what is a good library for it?


tempVarList =[]
prefixList = []

##To Do:
#Rename function
######
#reads csv, adds prefixes to the ids, calls makeRequest() and adds the result to the output RDF
def mergingCSV(filePath, consoleInputID, consoleOutputFilePathRDF):
    with open (filePath, 'r') as f:
        reader = csv.reader(f)
        for index, row in enumerate(reader):

            if (index == 0):
                for content in row:
                    prefixList.append(content)
            if (index == 1):

                for content in row:
                    tempVarList.append("\nprov:wasAttributedTo <" + content + ">;")
            idCount = int(consoleInputID) -1 + int(index)
            #print (row)
            if (index > 1):
                #idrow0 = "http://www.lgpn.ox.ac.uk/id/" + row[0]
                #idrow1 = "http://www.paregorios.org/resources/roman-elites/persons/" + row[1]
                newSnapID = "http://data.snapdrgn.net/person/"+str(idCount)+"/"
                with open (consoleOutputFilePathRDF, 'a') as snapfile:
                    snapfile.write("\n<" + newSnapID + ">")
                    snapfile.write("\na lawd:Person, snap:MergedResource ;")
                    for index, content in enumerate(prefixList):
                        print (content)
                        snapfile.write("\ndct:replaces <" + makeRequest(prefixList[index] + row[index]) + "> ;")
                    #snapfile.write("\ndct:replaces <" + makeRequest(idrow0) + "> ;")
                    #snapfile.write("\ndct:replaces <" + makeRequest(idrow1) + "> ;")
                    for item in tempVarList:
                        snapfile.write(item)
                    snapfile.write("\ndct:publisher <http://data.snapdrgn.net/person/> .\n")


##ToDo:
    # add sample Data
#####
#makes the SPARQL query, extracts the "value" out of the jsonObject

def makeRequest(idrow):
    query1 = 'PREFIX prov: <http://www.w3.org/ns/prov#> SELECT DISTINCT ?id { ?id prov:wasDerivedFrom <'+ idrow +'>}'
    data = {'query':query1}
    headers = {'Accept': 'application/sparql-results+json'}
    r = requests.get('https://snap.dighum.kcl.ac.uk/sparql/', params=data, headers=headers, verify=False)
    jsonData = r.json()
    if jsonData['results'].get('bindings'):
        return jsonData['results']['bindings'][0]['id']['value']
    else:
        return "SOMETHING IS WRONG AT THE PLAYGROUND"

#####
#cinstantiates the RDF and writes the prefixes needed for the triples
def instantiateTemplate(filePath):
    concfilePath = filePath
    with open (concfilePath , "w") as snapfile:
        snapfile.write("@prefix: <http://onto.snapdrgn.net/snap#> .\n@prefix dct: <http://purl.org/dc/elements/1.1/> .\n@prefix snap: <http://onto.snapdrgn.net/snap#> .\n@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n@prefix lawd: <http://lawd.info/ontology/> .\n")




consoleInput()
from django.shortcuts import HttpResponse
import requests
from django.shortcuts import render_to_response
#from django.views.decorators.cache import never_cache


#sparql_target = 'http://snap.dighum.kcl.ac.uk/sesame/repositories/snap'
sparql_target = 'http://localhost:9000/sparql/'
sparql_query_key = 'query'
sparql_prefixes_q1 = ['prov:<http://www.w3.org/ns/prov#>']
sparql_prefixes_q2 = [
    'foaf:<http://xmlns.com/foaf/0.1/>',
    'cito:<http://purl.org/spar/cito/>',
    'rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>',
    'lawd:<http://lawd.info/ontology/>',
    'dc:<http://purl.org/dc/elements/1.1/>',
    'schema:<http://schema.org/>',
    'rdfs:<http://www.w3.org/2000/01/rdf-schema#>',
    'cnt:<http://www.w3.org/2011/content#>',
    'bibo:<http://purl.org/ontology/bibo/>',
    'xsd:<http://www.w3.org/2001/XMLSchema#>',
    'owl:<http://www.w3.org/2002/07/owl#>',
    'dct:<http://purl.org/dc/terms/>',
    'prov:<http://www.w3.org/ns/prov#>',
   ]
sparql_prefixes_q3 = ['dct:<http://purl.org/dc/terms/>']
sparql_prefixes_q4 = [
    'snap:<http://onto.snapdrgn.net/snap#>',
    'cnt:<http://www.w3.org/2011/content#>',
    'rdfs:<http://www.w3.org/2000/01/rdf-schema#>',
    'lawd:<http://lawd.info/ontology/>'
    ]
sparql_id_prefix = 'http://data.snapdrgn.net/person/'

def index(request):
    return HttpResponse('ID number missing from url')

#@never_cache
def person(request, person_id, content_type='rdf'):
    query = ''
    for prefix in sparql_prefixes_q1:
        query += 'PREFIX ' + prefix + ' '
    query += 'SELECT DISTINCT ?id { <' + sparql_id_prefix + person_id + '> prov:wasDerivedFrom ?id }'

    data = {sparql_query_key: query}
    headers = {'Accept': 'application/sparql-results+json'}

    r = requests.get(sparql_target, params=data, headers=headers)
    jsonData = r.json()
    found_id = jsonData['results']['bindings'][0]['id']['value']

    query = ''
    for prefix in sparql_prefixes_q2:
        query += 'PREFIX ' + prefix + ' '

    if content_type == 'json':
        query += 'SELECT DISTINCT * WHERE {{<' + found_id + '> ?p ?o} UNION {?s ?p <'+ found_id + '>}}'
    else:
        query += 'DESCRIBE <' + found_id + '>'


    data = {sparql_query_key: query}
    if content_type == 'json':
        headers = {'Accept': 'application/sparql-results+json'}
    else:
        headers = {'Accept': 'application/rdf+xml'}

    r = requests.get(sparql_target, params=data, headers=headers) 

    if content_type == 'json':
        return HttpResponse(r.text, content_type='application/json')
    else:
        return HttpResponse(r.text, content_type='application/rdf+xml')

    #return HttpResponse(r.url)

def old_person_page(request, person_id):
    query = ''
    for prefix in sparql_prefixes_q1:
        query += 'PREFIX ' + prefix + ' '
    query += 'SELECT DISTINCT ?id { <' + sparql_id_prefix + person_id + '> prov:wasDerivedFrom ?id }'

    data = {sparql_query_key: query}
    headers = {'Accept': 'application/sparql-results+json'}

    r = requests.get(sparql_target, params=data, headers=headers)
    jsonData = r.json()
    
    if len(jsonData['results']['bindings']) < 1:
        return render_to_response('404.html', {"id": sparql_id_prefix + person_id, "debug": ''})
        
    found_id = jsonData['results']['bindings'][0]['id']['value']    

    query = ''
    for prefix in sparql_prefixes_q2:
        query += 'PREFIX ' + prefix + ' '
        
    query += 'SELECT DISTINCT ?s ?p ?o WHERE {{<' + found_id + '> ?p ?o} UNION {?s ?p <'+ found_id + '>}}'

    data = {sparql_query_key: query}
    
    headers = {'Accept': 'application/sparql-results+json'}

    r = requests.get(sparql_target, params=data, headers=headers)
    jsonData = r.json()

    results = jsonData['results']['bindings']

    return render_to_response('person.html', {"title": "SNAP: " + found_id, "results":results, "id":found_id})



def person_page(request, person_id):

    selected_id = sparql_id_prefix + person_id

    found_ids = []
    short_ids = []
    id_pairs = {}
    short_selected_id = ''
    short_id = ''
    
    for id in get_ids(selected_id):
        found_ids.append(id) 
                    #aggiunge l'id trovato alla lista dei record
                    #adds the id found in the list of records
        short_id=id.split("/")[-1]
                    #conserva solo l'ultima parte di url
                    #keeps just only the final part of the url
        if "#" in short_id:
            short_id=short_id.split('#')[0]
                    #elimina la parte a destra di #
                    #deletes what's on the right side of #
        short_ids.append(short_id)
                    #popola una lista
                    #populates a list
        id_pairs[id]=short_id
                    #compila un dizionario  prendendo id come chiave e short_id come valore
                    #compiles a dictionary taking id as key and short_id as value
        short_selected_id=selected_id.split('/')[-1]
        publisher='?'

    if len(short_ids)>1: 
        short_ids_j=", ".join(short_ids)     
        new_title=short_selected_id+" - "+short_ids_j
    else:
        new_title=short_selected_id+" - "+short_id
                    #terminato il ciclo di cui sopra, questa istruzione if-else consente di elaborare il titolo a seconda che ci siano uno o piu short_ids
                    #after having done the cicle, this instruction 'if-else' elaborates the title on the basis of the number of short_ids

    if len(found_ids) < 1:
        return render_to_response('404.html', {"id": selected_id, "debug": ''})

    subject_results = {}
    object_results = {}

    ids = ''
    results_check = []

    for found_id in found_ids:
        query = ''
        for prefix in sparql_prefixes_q2:
            query += 'PREFIX ' + prefix + ' '
        
        query += 'SELECT DISTINCT ?s ?p ?o WHERE {{<' + found_id + '> ?p ?o} UNION {?s ?p <'+ found_id + '>}}'

        data = {sparql_query_key: query}
    
        headers = {'Accept': 'application/sparql-results+json'}

        r = requests.get(sparql_target, params=data, headers=headers)
        jsonData = r.json()

        results = jsonData['results']['bindings']
    
        results_check.append(results)


        for row in results:
    
            p = ''
            o = ''
            s = ''
    
            if 'value' in row['p']:
                p = row['p']['value']
        
            if 'value' in row['o']:    
                o = row['o']['value']
            
            if 'value' in row['s']:    
                s = row['s']['value']
    
            if '#' in p:
                rel = p.split('#',1)[1]
            else:
                rel = p.rsplit('/', 1)[1]
        
            rel = rel.replace('-', '')
        
            if o == '':
                value = s 

                if (rel == 'wasDerivedFrom' and value != selected_id) or rel != 'wasDerivedFrom':
                    if rel in subject_results:
                        subject_results[rel].add(value)
                    else:
                        subject_results[rel] = set([value])            
            
            else:
                value = o  
        
                if rel in object_results:
                    object_results[rel].add(value)
                else:
                    object_results[rel] = set([value])   
        

    return render_to_response('person.html', {"title": "SNAP:" + new_title, "object_results": object_results, "subject_results": subject_results, "id_pairs": id_pairs, "url": selected_id, "debug": ''})


def test_page(request, person_id):

    selected_id = sparql_id_prefix + person_id

    found_ids = []
    short_ids = []
    id_pairs = {}
    short_selected_id = ''
    short_id = ''
    
    for id in get_ids(selected_id):
        found_ids.append(id) 
                    #aggiunge l'id trovato alla lista dei record
                    #adds the id found in the list of records
        short_id=id.split("/")[-1]
                    #conserva solo l'ultima parte di url
                    #keeps just only the final part of the url
        if "#" in short_id:
            short_id=short_id.split('#')[0]
                    #elimina la parte a destra di #
                    #deletes what's on the right side of #
        short_ids.append(short_id)
                    #popola una lista
                    #populates a list
        id_pairs[id]=short_id
                    #compila un dizionario  prendendo id come chiave e short_id come valore
                    #compiles a dictionary taking id as key and short_id as value
        short_selected_id=selected_id.split('/')[-1]
        publisher='?'

    if len(short_ids)>1: 
        short_ids_j=", ".join(short_ids)     
        new_title=short_selected_id+" - "+short_ids_j
    else:
        new_title=short_selected_id+" - "+short_id
                    #terminato il ciclo di cui sopra, questa istruzione if-else consente di elaborare il titolo a seconda che ci siano uno o piu short_ids
                    #after having done the cicle, this instruction 'if-else' elaborates the title on the basis of the number of short_ids
        
    if len(found_ids) < 1:
        return render_to_response('404.html', {"id": selected_id, "debug": get_ids(selected_id), "test": 'true'})
        
    subject_results = {}
    object_results = {}
#    bond_results = {}

    ids = ''
    results_check = []
    results_check2 = []

    for found_id in found_ids:
        query = ''
        for prefix in sparql_prefixes_q2:
            query += 'PREFIX ' + prefix + ' '
        
        query += 'SELECT DISTINCT ?s ?p ?o WHERE {{<' + found_id + '> ?p ?o} UNION {?s ?p <'+ found_id + '>}}'

        data = {sparql_query_key: query}
    
        headers = {'Accept': 'application/sparql-results+json'}

        r = requests.get(sparql_target, params=data, headers=headers)
        jsonData = r.json()

        results = jsonData['results']['bindings']
    
        results_check.append(results)

        for row in results:
    
            p = ''
            o = ''
            s = ''
    
            if 'value' in row['p']:
                p = row['p']['value']
        
            if 'value' in row['o']:    
                o = row['o']['value']
            
            if 'value' in row['s']:    
                s = row['s']['value']
    
    
            # add sparql query here to get extended info
            
            query2 = ''
            for prefix in sparql_prefixes_q4:
                query2 += 'PREFIX ' + prefix + ' '
        
            query2 += 'SELECT DISTINCT ?type, ?string, ?rel { <' + found_id + '> <' + p + '> ?x . ?x a ?type . OPTIONAL { ?x cnt:chars ?string } . OPTIONAL { ?x rdfs:label ?string } . OPTIONAL { ?x lawd:primaryForm ?string } . OPTIONAL { ?x snap:bondWith ?rel } . FILTER(STRSTARTS(STR(?type), "http://onto.snapdrgn.net/snap#") || STRSTARTS(STR(?type), "http://lawd.info/ontology/")) }'

            data2 = {sparql_query_key: query2}

            r2 = requests.get(sparql_target, params=data2, headers=headers)
            jsonData2 = r2.json()

            results2 = jsonData2['results']['bindings']

            results_check2.append(results2)

            type = ''
            string = ''
            related = ''
            expanded_info = []
            
            for row in results2:

                if 'value' in row['type']:
                    type = row['type']['value']
        
                if 'value' in row['string']:    
                    string = row['string']['value']
            
                if 'value' in row['rel']:    
                    related = row['rel']['value']
            
                expanded_info.append(string)
                
    
            if '#' in p:
                rel = p.split('#',1)[1]
            else:
                rel = p.rsplit('/', 1)[1]
        
            rel = rel.replace('-', '')
        
            if o == '':
                value = s 

                # KFL - Don't include wasDerivedFrom self in results (why is this coming up anyway???)
                if (rel == 'wasDerivedFrom' and value != selected_id) or rel != 'wasDerivedFrom':
                    if rel in subject_results:
                        if expanded_info == []:
                            subject_results[rel].add(value)
                        else:
                            subject_results[rel].union(set(expanded_info))
                    else:
                        if expanded_info == []:
                            subject_results[rel] = set([value])
                        else:
                            subject_results[rel] = set(expanded_info)            
            
            else:
                value = o  
        
                if rel in object_results:
                    if expanded_info == []:
                        object_results[rel].add(value)
                    else:
                        object_results[rel].union(set(expanded_info))
                else:
                    if expanded_info == []:
                        object_results[rel] = set([value])
                    else:
                        object_results[rel] = set(expanded_info)              
            

    return render_to_response('person.html', {"title": "SNAP:" + new_title, "object_results":object_results, "subject_results":subject_results, "id_pairs": id_pairs, "url": selected_id, "debug": '', "test": 'true'})
    
def get_ids(selected_id):
    
    query = ''
    for prefix in sparql_prefixes_q1:
        query += 'PREFIX ' + prefix + ' '
    query += 'SELECT DISTINCT ?id { <' + selected_id + '> prov:wasDerivedFrom ?id }'

    data = {sparql_query_key: query}
    headers = {'Accept': 'application/sparql-results+json'}

    r = requests.get(sparql_target, params=data, headers=headers)
    jsonData = r.json()
    
    found_ids = []
    
    if len(jsonData['results']['bindings']) > 0:
        found_ids.append(jsonData['results']['bindings'][0]['id']['value'])
        
        return found_ids
    
    
    query = ''
    for prefix in sparql_prefixes_q3:
        query += 'PREFIX ' + prefix + ' '
        
    query += 'SELECT DISTINCT ?id {<' + selected_id + '> dct:replaces ?id }'
        
    data = {sparql_query_key: query}
    headers = {'Accept': 'application/sparql-results+json'}

    r = requests.get(sparql_target, params=data, headers=headers)
    jsonData = r.json()
    
    
    for row in jsonData['results']['bindings']:
        found_ids.append(row['id']['value'])
        
        for id in get_ids(row['id']['value']):
            found_ids.append(id)
    
    return found_ids

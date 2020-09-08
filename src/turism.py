# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
import json
from SPARQLWrapper import SPARQLWrapper, JSON
import re

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?monta_a ?monta_aLabel ?coordenadas WHERE {
        SERVICE wikibase:label { bd:serviceParam wikibase:language "es". }
        ?monta_a wdt:P31 wd:Q8502;
            wdt:P131 wd:Q5813.
        OPTIONAL { ?monta_a wdt:P625 ?coordenadas. }
        }"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

#print(results["results"]["bindings"])

patron = "Q.*"

for result in results["results"]["bindings"]:

    if not (re.search(patron,str(result['monta_aLabel']['value']) )):
        print(result['coordenadas']['value'])


Mountains_JSON = {}
Mountains_JSON['mountains'] = []


# for result in results["results"]["bindings"]:
#     Mountains_JSON['mountains'].append({
#         'name_mountain': result['monta_aLabel']['value'],
#         'coordenada': result['coordenadas']['value']
#     })


# print("*******************************************************")
# print(Mountains_JSON)

with open('data_mountains.json', 'w') as file:
    json.dump(Mountains_JSON, file, indent=4)

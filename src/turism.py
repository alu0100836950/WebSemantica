# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
import json
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?playa ?playaLabel ?coordenadas WHERE {
  ?playa wdt:P31 wd:Q40080.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "es". }
  ?playa wdt:P131 wd:Q5813.
  OPTIONAL { ?playa wdt:P625 ?coordenadas. }
}"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

#for result in results["results"]["bindings"]:
#    print(result['playaLabel']['value'])


Beach_JSON = {}
Beach_JSON['beach'] = []

for result in results["results"]["bindings"]:
    Beach_JSON['beach'].append({
        'name_beach': result['playaLabel']['value'],
        'coordenada': result['coordenadas']['value']
    })

print("*******************************************************")
print(Beach_JSON)

with open('data.json', 'w') as file:
    json.dump(Beach_JSON, file, indent=4)

from flask import Flask
from flask import render_template, request, redirect, url_for
from SPARQLWrapper import SPARQLWrapper, JSON
import sys, json


app = Flask(__name__)

endpoint_url = "https://query.wikidata.org/sparql"


def get_results(endpoint_url, query):

    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert() 


#
### Método para devolver un JSON con los datos que queremos de las playas
#
def data_json_beach(results):

    Beach_JSON = {}
    Beach_JSON['beach'] = []


    for result in results["results"]["bindings"]:
        Beach_JSON['beach'].append({
            'name_beach': result['playaLabel']['value'],
            'coordenada': result['coordenadas']['value']
        })


    return Beach_JSON

#
### Método para devolver un JSON con los datos que queremos de las playas
#
def data_json_mountains(results):

    Mountains_JSON = {}
    Mountains_JSON['mountains'] = []


    for result in results["results"]["bindings"]:
        Mountains_JSON['beach'].append({
            'name_mountain': result['monta_aLabel']['value'],
            'coordenada': result['coordenadas']['value']
        })


    return Mountains_JSON


#
### Este método recoge la opcion escogida en la web y crea la consulta y devuelte
### los datos parseados a JSON
#
def query_list(selected):

    print('usted ha elegido ' + selected)
    
    ## Consulta de las playas dee canarias
    if selected == 'beach':


        query = """SELECT ?playa ?playaLabel ?coordenadas WHERE {
        ?playa wdt:P31 wd:Q40080.
        SERVICE wikibase:label { bd:serviceParam wikibase:language "es". }
        ?playa wdt:P131 wd:Q5813.
        OPTIONAL { ?playa wdt:P625 ?coordenadas. }
        }"""

        results = get_results(endpoint_url, query)
        results_parse = data_json_beach(results) # llamamos a la funcion json

        ## Modificamos el campo coordenada para obtener los puntos en orden y limpios
        for item in results_parse['beach']:
            pointStr = item['coordenada'].replace('Point(', '').replace(')', '')
            x = pointStr.split(' ')
            item['coordenada'] = createPoint(x)
        

        return results_parse
        
    ## Consulta para las montañasn de canarias
    if selected == 'mountains':

        query = """SELECT ?monta_a ?monta_aLabel ?coordenadas WHERE {
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        ?monta_a wdt:P31 wd:Q8502;
            wdt:P131 wd:Q5813.
        OPTIONAL { ?monta_a wdt:P625 ?coordenadas. }
        }"""

        results = get_results(endpoint_url, query)
        results_parse = data_json_mountains(results)


        for item in results_parse['mountains']:
            pointStr = item['coordenada'].replace('Point(', '').replace(')', '')
            x = pointStr.split(' ')
            item['coordenada'] = createPoint(x)
        

        return results_parse


#
### Modificamos los puntos de las coordenadas en el orden correcto
#
def createPoint(points):
    return f'{points[1]},{points[0]}'
    

@app.route('/', methods=["GET", "POST"])
def index():
    
    validate = 'opcion no válida'

    if request.method == 'POST':
        select = request.form.get('select')
        
        search = query_list(str(select))

        ok='ok'

        if select == 'beach' or 'mountains':
            return render_template('index.html', search =search, select=select, ok=ok)
        return render_template('index.html', validate=validate)    
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run('127.0.0.1', 4000, debug=False)

# Práctica Web Semántica

#### Alberto Martín Núñez

## Índice de contenidos

1. [Objetivo de la práctica](#id1)
2. [Aplicacion Web](#id2)
    1. [Herramientas utilizadas](#id2.1)
    2. [Metodología y Resultado Final](#id2.2)
3. [Conclusiones](#id3)


## Objetivo de la práctica <a name="id1"></a>

El objetivo para esta práctica consiste en construir una pequeña aplicación web que explote las consultas de **wikidata** para ofrecer un servicio en un campo concreto: turismo, economóa, seguros, aficiones, etcetera. 

Se trata de buscar una aplicacióm donde la **web semántica** sea relevante. La aplicación deberá lanzar consultas Sparql contra wikipedia y mostrar los resultados.

Para nuestro caso vamos a centrarnos en el campo del *turismo*, en donde ofreceremos una pequeña web para encontrar lugares de interés como playas y montañas de las islas canarias. De esta forma cualquier persona podría acceder y escoger que lugar visitar.


## Aplicación Web <a name="id3"></a>

A continuación se explicará las herramientas que se han utilizado para crear la aplicacion web, asi como la metodología empleada y el resultado que se ha obtenido.


### Herramientas utilizadas <a name="id3.1"></a>

Para la creación de la aplicación web he utilizado **flask**, un "micro" framework de **python** que nos permite crear de manera muy sencilla aplicaciones web usando **python** como lenguaje de programación.

Para obtener datos utilizamos **wikidata**, una base de datos abierto y gratuito que recopila datos estructurados. Para poder acceder a estos datos y lanzar consultas a la wikidata usaremos **SPARQL**, que es el lenguaje de consultas estandar.

Wikidata nos pone a nuestra disposición una aplicacion denominada *Wikidata Query Service* para realizar consultas a la propia wikidata de una forma limpia y con un asistente de consultas.

![Query Service](./static/img/QUERY_SERVICE.jpeg)

### Metológía y Resultado Final <a name="id3.1"></a>

Cómo nuestra aplicación web consistirá en ofrecer lugares de las islas canarias a los que visitar, primeramente debemos conocer de que forma podemos crear la consulta para obtener los datos que queremos representar.

#### Obteniendo los datos de wikidata

Nuestra consulta consistirá en obtener el nombre de las montañas y las coordenadas de la misma. De esta forma mostraremos en la web una tabla con las distintas montañas y con sus respectivas ubicaciones, las cuales, a través de un enlace nos llevará a la ubicacion de *Google Maps*

Usaremos como ejemplo el objeto *montañas* de las islas canarias para mostrar el procedimiento:


![Code Mountain](./static/img/code_mountain.jpeg)

Una vez que hemos localizado el objeto importante de nuestra consulta, utilizamos el asistente de consultas de wikidata para crear la consulta y visualizar los resultamos que queremos obtener:

![Query Mountain](./static/img/query_mountain.jpeg)

AHora que tenemos la consulta realizada y los datos obtenidos, wikidata nos ofrece la oportunidad de exportar el codigo para implantarlo en nuestro entorno. Una de las formas más sencillas es utilizar un **iframe** y añadirlo al *HTML*. Pero como en mi caso estoy usando *python* he escogido el codigo que nos ofrece en el propio lenguaje que en lo siguiente:

```python
# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

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

for result in results["results"]["bindings"]:
    print(result)
```

Podemos destacar la variable *query*, en donde tenemos la consulta que hemos realizado en el asistente y el método *get_results* dónde se lanza la consulta contra Wikidata.

#### Manipulando los datos recogidos

Ahora que hemos obtenido los datos los manipularemos de tal forma que podamos mostrar lo necesario en nuestra web. Para ello se crea un método que recoge los datos de la consulta y devuelve un JSON con los propios datos que vamos a representar. Lo hacemos de la siguiente forma:

```python
#
### Método para devolver un JSON con los datos que queremos de las playas
#
def data_json_mountains(results):


    Mountains_JSON = {}
    Mountains_JSON['mountains'] = []

    patron = "Q.*"

    for result in results["results"]["bindings"]:
        if not (re.search(patron,str(result['monta_aLabel']['value']) )):
        
            Mountains_JSON['mountains'].append({
                'name_mountain': result['monta_aLabel']['value'],
                'coordenada': result['coordenadas']['value']
            })


    return Mountains_JSON

```

Ahora tendriamos un *json* con la siguiente estructura:

```json
{
    "mountains": [
        {
            "name_mountain": "Roque de Iguala",
            "coordenada": "Point(-17.319444444 28.058611111)"
        },
        {
            "name_mountain": "Atalaya de los Ingleses",
            "coordenada": "Point(-16.15 28.531944444)"
        },
    ]
}
```

## Conclusiones <a name="id4"></a>
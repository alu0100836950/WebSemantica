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

Wikidata nos pone a nuestra disposicion una aplicacion denominada *Wikidata Query Service* para realizar consultas a la propia wikidata de una forma limpia y con un asistente de consultas.

![Query Service](/static/img/QUERY_SERVICE.jpeg)

### Metológía y Resultado Final <a name="id3.1"></a>

## Conclusiones <a name="id4"></a>
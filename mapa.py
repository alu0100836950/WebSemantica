import folium

#las coordenadas de wikidata hay que ponerlas al reves
mapa = folium.Map(location=[28.566667, -16.2], zoom_start=15)

path = 'playa.html'

mapa.save(path)


class SPARQLQueryDispatcher {
	constructor( endpoint ) {
		this.endpoint = endpoint;
	}

	query( sparqlQuery ) {
		const fullUrl = this.endpoint + '?query=' + encodeURIComponent( sparqlQuery );
		const headers = { 'Accept': 'application/sparql-results+json' };

		return fetch( fullUrl, { headers } ).then( body => body.json() );
	}
}

let search = 'playa';

const endpointUrl = 'https://query.wikidata.org/sparql';
const sparqlQuery = `SELECT ?${search} ?playaLabel ?coordenadas WHERE {
  ?playa wdt:P31 wd:Q40080.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "es". }
  ?playa wdt:P131 wd:Q5813.
  OPTIONAL { ?playa wdt:P625 ?coordenadas. }
}`;

const queryDispatcher = new SPARQLQueryDispatcher( endpointUrl );
queryDispatcher.query( sparqlQuery ).then( console.log );

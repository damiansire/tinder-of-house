ID de mi departamento:

"id": "TUxVUENBTnMxNzliYw",
"name": "Canelones"


"id": "TUxVQ0FUTDI1ZmY5",
"name": "Atlántida"


formas de obtener la informacion que no anduvieron:
(latitud, longitud)
longitud minima
-55.781099
longitud maxima
-55.699903
latitud minima
-34.782173
latitud maxima
-34.752067
lat:latitudMinima_latitudMaxima
lon:lonMinima_lonMaxima
lat:-34.782173_-34.752067,lon:-55.781099_-55.699903
### con dos diferentes (de mas chica a mas grande)
curl -X GET https://api.mercadolibre.com/sites/MLU/search?item_location=lat:-34.782173_-34.752067,lon:-55.781099_-55.699903&category=MLU1459&limit=20

### de mas grande a mas chica
curl -X GET https://api.mercadolibre.com/sites/MLU/search?item_location=lat:-34.752067_-34.782173,lon:-55.699903_-55.781099&category=MLU1459&limit=20


### con la misma
https://api.mercadolibre.com/sites/MLU/search?item_location=lat:-34.782173_-34.782173,lon:-55.781099_-55.781099&category=MLU1467&limit=20

## Busco por texto
https://api.mercadolibre.com/sites/MLU/search?q=alquiler%20casa%20en%20atlantida&limit=2



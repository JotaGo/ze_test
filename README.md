## Primeros pasos
### Preparando el entorno
Para inicializar el servidor, primero debemos instalar python3 en nuestro sistema operativo, si el equipo es windows
dirigirse a la pagina oficial : https://www.python.org/downloads/ de otra forma si el sistema operativo es linux instalar
con el comando sudo "apt-get install python3".

Luego de instalar python3, procedemos a instalar las librerias que se ocuparan para la ejecución del servidor, para esto
ocuparemos el comando "pip3 install -p requirements.txt", una vez finalizado este proceso, procederemos a instalar mongodb
para esto si nos dirigimos a la pagina oficial y seguimos las instrucciones:
https://docs.mongodb.com/manual/administration/install-community/
Seleccionamos el sistema operativo que tenemos y seguimos los pasos que nos muestran.

Por ultimo importamos el documento .json adjunto en el paquete el cual se toma como referencia para la base de datos para esto
ejecutamos el siguiente comando en la terminal

mongoimport --db areas --collection areas --file <file_path>\areas.json 

donde en <file_path> tiene que ir la ruta donde se encuentra el archivo

## Guia de uso

### Buscar area por ID
Para buscar un area por id se debe utilizar un request con metodo GET a la direccion 
http://127.0.0.1:5000/areas/<id>
donde en <id> escribimos el numero del id del area que queremos buscar

### Crear un nuevo partner
Para crear un nuevo partner debemos utilizar un request con el metodo POST a la direccion
http://127.0.0.1:5000/new_partner
donde el body debe ser en formato geojson con un Documento y ID unico 
ejemplo:
{"pdvs": [
    {
       "id": "52",
       "tradingName": "Adega Osasco",
       "ownerName": "Ze da Ambev",
       "document": "02.453.716/00213",
       "coverageArea": {
          "type": "MultiPolygon",
          "coordinates": [
             [
                [
                   [
                      -43.25346,
                      -22.99065
                   ],
                   [
                      -43.29599,
                      -22.98283
                   ],
                   [
                      -43.3262,
                      -22.96481
                   ],
                   [
                      -43.33427,
                      -22.96402
                   ],
                   [
                      -43.33616,
                      -22.96829
                   ],
                   [
                      -43.342,
                      -22.98157
                   ],
                   [
                      -43.34817,
                      -22.97967
                   ],
                   [
                      -43.35142,
                      -22.98062
                   ],
                   [
                      -43.3573,
                      -22.98084
                   ],
                   [
                      -43.36522,
                      -22.98032
                   ],
                   [
                      -43.36696,
                      -22.98422
                   ],
                   [
                      -43.36717,
                      -22.98855
                   ],
                   [
                      -43.36636,
                      -22.99351
                   ],
                   [
                      -43.36556,
                      -22.99669
                   ]
                ]
             ]
          ]
       },
       "address": {
          "type": "Point",
          "coordinates": [
             -43.297337,
             -23.013538
          ]
       }
    }
  ]
}

### partner mas cercano a una ubicación
Para determinar cual partnert se tiene mas cercano a una ubicación se debe utilizar un request con metodo GET
a la siguiente direccion:
http://127.0.0.1:5000/nearest_location/<lat+lon>
en donde tenemos que ingresar en <lat+lon> las coordenadas especificas que queramos en el siguiente orden
latiud+longitud, ejemplo:
http://127.0.0.1:5000/nearest_location/-40.36539+-20.01928

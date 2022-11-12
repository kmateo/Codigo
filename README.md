# Gentrificación en la ciudad de Madrid.
## Estudio de los factores que provocan la gentrificación en la ciudad de Madrid.
### Kevin Mateo García

## Contenido del repositorio:

- README.md -- Instrucciones de uso del programa.
- datos/ -- Carpeta que contiene todos los datasets de origen, procesados y finales para cargar en CARTO.
Se incluyen los datos que no se han podido obtener de forma programática, como los datasets con la información de barrios y distritos, 
- obtain_data -- Código para obtener automáticamente datos de portalestadistico.es e idealista.
- transform -- Código para limpiar y procesar los datos brutos.
- ML/ -- Código que aplica el algoritmo de ML a los datos previamente preparados.
- requirements.txt -- Fichero con los paquetes necesarios para lanzar el programa.
- main.py -- Código principal para lanzar el programa.

## Instrucciones de uso.

1. Instalar requirements.txt.
```
pip install -r requirements.txt
```
2. Lanzar main.py y seguir el menú que aparece en el programa.
```
python3 main.py
```
3. El orden lógico sería seguir el menú en orden: obtención, limpieza, generación de dataset para CARTO y aplicación de ML.


import pandas as pd
from obtain_data.portalestadistico import import_portal_estadistico
from obtain_data.idealista import import_historico_idealista
from transform.datasets_for_carto import generate_dataset_for_carto, generate_datasets_kpis
from ML.kmeans import apply_kmeans
import sys,os

ans=True
while ans:
    os.chdir(os.path.dirname(__file__))
    print("""
    ------------------------------------------------------
        1.Obtener datos de portalestadistico.es por barrio
        2.Obtener datos de idealista.
        3.Limpiar datos para generar datasets de kpis individuales.
        4.Generar dataset para cargar en CARTO.
        5.Aplicar algoritmo de clusterización.
        6.Salir
    ------------------------------------------------------
    """)
    ans=input("Selecciona una opción: ")
    if ans=="1":
        print("\nSe van a obtener los datos por barrio de portalestadistico.es \n")
        import_portal_estadistico()
        print("Los datos se encuentran en el directorio datos")
    elif ans=="2":
        print("\n Obteniendo datos históricos de idealista \n")
        import_historico_idealista()
        print("Los datos se encuentran en el directorio datos")
    elif ans=="3":
        print("\n Generando datasets de las distintas mediciones de forma individual")
        generate_datasets_kpis()
        print("Los datos se encuentran en el directorio datos/procesado")
    elif ans=="4":
        print("\n Generando dataset con todas las mediciones cruzadas para cargar en CARTO")
        generate_dataset_for_carto()
        print("Se ha generado el dataset en el directorio datos/carto")
    elif ans=="5":
        print("\n Aplicando algoritmo kmeans para realizar una clusterización")
        apply_kmeans()
        print('Se han generado distintos datasets en el directorio datos/carto')
    elif ans=="6":
        print("\n Fin del proyecto!") 
        ans = None
    else:
       print("\n Introduce una opción válida \n")
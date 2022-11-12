import csv
import requests
import pandas as pd 

URL_POBLACION = "http://portalestadistico.com/municipioencifras/proceso_descarga_excel_csv.aspx?pn=madrid&pc=ZTV21&idp=35&Id_Celda_Fila_Plantilla=8373&Id_Territorio=28079BAR0X&Id_Territorio_Padre=28079&idioma=1&Tipo_Fichero_Generado=csv"
URL_MIGRACION = "http://portalestadistico.com/municipioencifras/proceso_descarga_excel_csv.aspx?pn=madrid&pc=ZTV21&idp=35&Id_Celda_Fila_Plantilla=8391&Id_Territorio=28079BAR0X&Id_Territorio_Padre=28079&idioma=1&Tipo_Fichero_Generado=csv"
URL_PARADOS = "http://portalestadistico.com/municipioencifras/proceso_descarga_excel_csv.aspx?pn=madrid&pc=ZTV21&idp=35&Id_Celda_Fila_Plantilla=8393&Id_Territorio=28079BAR0X&Id_Territorio_Padre=28079&idioma=1&Tipo_Fichero_Generado=csv"
URL_AUTONOMOS = "http://portalestadistico.com/municipioencifras/proceso_descarga_excel_csv.aspx?pn=madrid&pc=ZTV21&idp=35&Id_Celda_Fila_Plantilla=8941&Id_Territorio=28079BAR0X&Id_Territorio_Padre=28079&idioma=1&Tipo_Fichero_Generado=csv"
URL_RENTA = "http://portalestadistico.com/municipioencifras/proceso_descarga_excel_csv.aspx?pn=madrid&pc=ZTV21&idp=35&Id_Celda_Fila_Plantilla=8943&Id_Territorio=28079BAR0X&Id_Territorio_Padre=28079&idioma=1&Tipo_Fichero_Generado=csv"


urls = [["poblacion", URL_POBLACION], ["migracion", URL_MIGRACION],
        ["parados", URL_PARADOS], ["autonomos", URL_AUTONOMOS], ["renta", URL_RENTA]]

def import_portal_estadistico():
    bar1_df = pd.read_csv('datos/raw/barrios.csv', decimal=',', delimiter=';',header=0).rename(columns={'COD_BAR':'codbar'})
    bar2_df = pd.read_csv('datos/raw/barrios-2.csv', delimiter=',',header=0)
    bar_df = pd.merge(bar1_df, bar2_df, on='codbar')


    for index,barrio in bar_df.iterrows():
        numBarrio= barrio['codbar']
        numDistrito = barrio['coddistrit']
        print(bar_df.loc[bar_df['codbar'] == numBarrio, ['BARRIO_MAY']])
        for url in urls:
            print('Descargando ' + url[0])
            if numBarrio < 100:
                df = pd.read_csv(url[1].replace('BAR0X', 'BAR0' + str(numBarrio)), delimiter=';', decimal=',', encoding='utf-8', on_bad_lines='skip', header=2, encoding_errors='ignore')
            else:
                df = pd.read_csv(url[1].replace('BAR0X', 'BAR' + str(numBarrio)), delimiter=';', decimal=',', encoding='utf-8', on_bad_lines='skip', header=2, encoding_errors='ignore')

            df['codigo_barrio'] = numBarrio
            df['codigo_distrito'] = numDistrito
            df.to_csv('datos/raw/' + url[0] + '/' + str(numBarrio) + '.csv')  
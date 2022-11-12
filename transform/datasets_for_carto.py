import os
import glob
import pandas as pd
import re


def generate_datasets_kpis():
    #AUTONOMOS
    print("Preparando datos de autónomos...\n")
    os.chdir("datos/raw/autonomos")
    df_autonomos = pd.DataFrame()
    filenames = [file for file in os.listdir() if file.endswith(".csv")]
    for file in filenames:
        df = pd.read_csv(file, header=0, encoding_errors='ignore').drop(columns=['Unnamed: 0', 'Periodos', 'Unnamed: 3'])
        df = df.rename(columns={'Ao':'Anyo'})
        df = df.melt(id_vars=["Anyo", "codigo_barrio","codigo_distrito"], 
                var_name="Nombre_barrio", 
                value_name="autonomos")
        df['fecha'] = pd.to_datetime(dict(year=df['Anyo'], month=1, day=1))
        df_autonomos= df_autonomos.append(df)
                                                                        
    #df_final = pd.merge(df_barrios, df_autonomos, on='codigo_barrio')[['codigo_barrio','BARRIO_MAY','NOMDIS','the_geom','shape_area','shape_len','Anyo','codigo_distrito','autonomos','fecha']]
    df_autonomos = df_autonomos.groupby(['Anyo','codigo_distrito', 'codigo_barrio'])['autonomos'].sum()
    df_autonomos.to_csv( "../../procesado/autonomos.csv", index=True, encoding='utf-8')
    print("Listo!\n")

    #MIGRACION
    print("Preparando datos de migracion...\n")
    os.chdir("../migracion")
    df_migracion = pd.DataFrame()
    filenames = [file for file in os.listdir() if file.endswith(".csv")]
    for file in filenames:
        df = pd.read_csv(file, header=0, encoding_errors='ignore').drop(columns=['Unnamed: 0', 'Periodos', 'Madrid', 'Unnamed: 4'])
        df = df.rename(columns={'Ao':'Anyo'})
        df = df.melt(id_vars=["Anyo", "codigo_barrio","codigo_distrito"], 
                var_name="Nombre_barrio", 
                value_name="tasa_extranjeros")
        df['fecha'] = pd.to_datetime(dict(year=df['Anyo'], month=1, day=1))
        df_migracion= df_migracion.append(df)

    #df_final = pd.merge(df_barrios, df_migracion, on='codigo_barrio')[['codigo_barrio','BARRIO_MAY','NOMDIS','tasa_migracion','Anyo','codigo_distrito','the_geom','shape_area','shape_len','fecha']]
    df_migracion = df_migracion.loc[df_migracion['tasa_extranjeros'] > 0]
    df_migracion = df_migracion.groupby(['Anyo','codigo_distrito', 'codigo_barrio'])['tasa_extranjeros'].sum()

    df_migracion.to_csv( "../../procesado/migracion.csv", index=True, encoding='utf-8')
    print("Listo!\n")

    #PARADOS
    print("Preparando datos de parados...\n")
    os.chdir("../parados")
    filenames = [file for file in os.listdir() if file.endswith(".csv")]
    df_test = pd.read_csv(filenames[0], header=0, encoding_errors='ignore')
    df_parados = pd.DataFrame()
    for file in filenames:
        df = pd.read_csv(file, header=0, encoding_errors='ignore').drop(columns=['Unnamed: 0', 'Unnamed: 3'])
        df = df.rename(columns={'Ao':'Anyo'})
        df = df.melt(id_vars=["Anyo", "codigo_barrio","codigo_distrito", "Periodos"], 
                var_name="Nombre_barrio", 
                value_name="parados")
        df = df.replace({'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4, 'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8, 'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12})
        df['fecha'] = pd.to_datetime(dict(year=df['Anyo'], month=df['Periodos'], day=1))

        df_parados= df_parados.append(df)
    #df_final = pd.merge(df_barrios, df_parados, on='codigo_barrio')[['codigo_barrio','BARRIO_MAY','NOMDIS','parados','Anyo','codigo_distrito','the_geom','shape_area','shape_len','fecha']]
    df_parados = df_parados.groupby(['Anyo','codigo_distrito', 'codigo_barrio'])['parados'].sum()
    df_parados.to_csv( "../../procesado/parados.csv", index=True, encoding='utf-8')
    print("Listo!\n")

    #POBLACION
    print("Preparando datos de poblacion...\n")
    os.chdir("../poblacion")
    df_poblacion = pd.DataFrame()
    filenames = [file for file in os.listdir() if file.endswith(".csv")]
    for file in filenames:
        df = pd.read_csv(file, header=0, encoding_errors='ignore').drop(columns=['Unnamed: 0', 'Periodos', 'Unnamed: 3'])
        df = df.rename(columns={'Ao':'Anyo'})
        df = df.melt(id_vars=["Anyo", "codigo_barrio","codigo_distrito"], 
                var_name="Nombre_barrio", 
                value_name="poblacion")
        df['fecha'] = pd.to_datetime(dict(year=df['Anyo'], month=1, day=1))

        df_poblacion= df_poblacion.append(df)
    #df_final = pd.merge(df_barrios, df_poblacion, on='codigo_barrio')[['codigo_barrio','BARRIO_MAY','NOMDIS','poblacion','Anyo','codigo_distrito','the_geom','shape_area','shape_len','fecha']]
    df_poblacion = df_poblacion.groupby(['Anyo','codigo_distrito', 'codigo_barrio'])['poblacion'].sum()
    df_poblacion.to_csv( "../../procesado/poblacion.csv", index=True, encoding='utf-8')

    print("Listo!\n")

    #RENTA
    print("Preparando datos de renta...\n")
    os.chdir("../renta")
    df_renta = pd.DataFrame()
    filenames = [file for file in os.listdir() if file.endswith(".csv")]
    for file in filenames:
        df = pd.read_csv(file, header=0, encoding_errors='ignore').drop(columns=['Unnamed: 0', 'Periodos', 'Unnamed: 4', 'Madrid'])
        df = df.rename(columns={'Ao':'Anyo'})
        df = df.replace(',','.')
        df = df.melt(id_vars=["Anyo", "codigo_barrio","codigo_distrito"], 
                var_name="Nombre_barrio", 
                value_name="renta")
        df['fecha'] = pd.to_datetime(dict(year=df['Anyo'], month=1, day=1))

        df_renta= df_renta.append(df)
    #df_final = pd.merge(df_barrios, df_renta, on='codigo_barrio')[['codigo_barrio','BARRIO_MAY','NOMDIS','renta','Anyo','codigo_distrito','the_geom','shape_area','shape_len','fecha']]
    df_renta = df_renta.groupby(['Anyo','codigo_distrito', 'codigo_barrio'])['renta'].sum()
    df_renta.to_csv( "../../procesado/renta.csv", index=True, encoding='utf-8')
    print("Listo!\n")

    #INCIDENTES
    print("Preparando datos de incidentes...\n")
    os.chdir("../incidentes")
    filenames_xlsx = [file for file in os.listdir() if file.endswith(".xlsx")]
    filenames_xls = [file for file in os.listdir() if file.endswith(".xls")]
    df_incidentes = pd.DataFrame()
    for file in filenames_xlsx:
        df = pd.read_excel(file, sheet_name='SEGURIDAD', header=2)
        df['codigo_distrito'] = [x for x in range (1,len(df)+1)]
        df = df.loc[df['codigo_distrito'] <= 21]
        df['Anyo'] = re.search(r'\d{4}', file).group()
        df['Mes'] =  re.findall('(ENERO|FEBRERO|MARZO|ABRIL|MAYO|JUNIO|JULIO|AGOSTO|SEPTIEMBRE|OCTUBRE|NOVIEMBRE|DICIEMBRE)', file.upper())[0].capitalize()
        df = df.replace({'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4, 'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8, 'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12})
        df['incidentes_por_distrito'] = df.iloc[:,1:5].sum(axis=1)
        df['fecha'] = pd.to_datetime(dict(year=df['Anyo'], month=df['Mes'], day=1))
        df_incidentes= df_incidentes.append(df[['codigo_distrito','incidentes_por_distrito','Anyo','fecha']])
    for file in filenames_xls:
        df = pd.read_excel(file, sheet_name='SEGURIDAD',engine='xlrd', header=2)
        df['codigo_distrito'] = [x for x in range (1,len(df)+1)]
        df = df.loc[df['codigo_distrito'] <= 21]
        df['Anyo'] = re.search(r'\d{4}', file).group()
        df['Mes'] =  re.findall('(ENERO|FEBRERO|MARZO|ABRIL|MAYO|JUNIO|JULIO|AGOSTO|SEPTIEMBRE|OCTUBRE|NOVIEMBRE|DICIEMBRE)', file.upper())[0].capitalize()
        df = df.replace({'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4, 'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8, 'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12})
        df['incidentes_por_distrito'] = df.iloc[:,1:5].sum(axis=1)
        df['fecha'] = pd.to_datetime(dict(year=df['Anyo'], month=df['Mes'], day=1))
        df_incidentes= df_incidentes.append(df[['codigo_distrito','incidentes_por_distrito','Anyo','fecha']])

    df_incidentes = df_incidentes.groupby(['Anyo','codigo_distrito'])['incidentes_por_distrito'].sum()
    #dist_df = pd.read_csv('../distritos.csv',header=0).rename(columns={'coddistrit':'cod_distrito'})
    #df_final = pd.merge(dist_df, df_incidentes, on='cod_distrito')[['nombre','the_geom','Anyo','cod_distrito','incidentes_por_distrito','fecha']]
    df_incidentes.to_csv('../../procesado/incidentes.csv', index=True)

    print("Listo!\n")

    #TAMAÑO DEL HOGAR
    print("Preparando datos del tamaño de los hogares...\n")
    os.chdir("../")
    df = pd.read_csv('panel_indicadores_distritos_barrios.csv',dtype={'cod_distrito': 'Int32', 'cod_barrio': 'Int32'}, delimiter=';', encoding='utf-8', encoding_errors='replace')
    df_hogar = df.loc[df['indicador_completo'] == 'Tama�o medio del hogar      ' ]
    df_hogar = df_hogar.rename(columns={'valor_indicador':'tamanyo_hogar','cod_distrito':'codigo_distrito', 'fecha_indicador':'fecha', 'cod_barrio':'codigo_barrio'})
    df_hogar['Anyo'] = pd.DatetimeIndex(df_hogar['fecha']).year
    df_hogar = df_hogar.loc[df_hogar['codigo_barrio'] != '']
    df_hogar['tamanyo_hogar'] = [x.replace(',', '.') for x in df_hogar['tamanyo_hogar']]
    df_hogar['tamanyo_hogar'] = df_hogar['tamanyo_hogar'].astype(float)
    df_hogar = df_hogar[['Anyo','codigo_distrito','codigo_barrio','fecha','tamanyo_hogar']]
    #df_final = pd.merge(df_barrios, df_hogar, on='codigo_barrio')[['codigo_barrio','BARRIO_MAY','NOMDIS','tamanyo_hogar','Anyo','cod_distrito','the_geom','shape_area','shape_len','fecha']]
    df_hogar = df_hogar.groupby(['Anyo','codigo_distrito', 'codigo_barrio'])['tamanyo_hogar'].sum()
    df_hogar.to_csv('../procesado/tamanyo_hogar.csv', index=True) 
    print("Listo!\n")

    #TOTAL DE VIVIENDAS
    print("Preparando datos de viviendas...\n")

    df_viviendas = df.loc[df['indicador_completo'] == 'Total hogares']
    df_viviendas = df_viviendas.rename(columns={'valor_indicador':'total_viviendas','cod_distrito':'codigo_distrito','fecha_indicador':'fecha','cod_barrio':'codigo_barrio'})
    df_viviendas['Anyo'] = pd.DatetimeIndex(df_viviendas['fecha']).year
    df_viviendas = df_viviendas.loc[df_viviendas['codigo_barrio'] != '']
    df_viviendas['total_viviendas'] = [x.replace('.', '') for x in df_viviendas['total_viviendas']]
    df_viviendas['total_viviendas'] = df_viviendas['total_viviendas'].astype(float)
    df_viviendas = df_viviendas[['Anyo','codigo_distrito','codigo_barrio','fecha','total_viviendas']]
    #df_final = pd.merge(df_barrios, df_viviendas, on='codigo_barrio')[['codigo_barrio','BARRIO_MAY','NOMDIS','total_viviendas','Anyo','cod_distrito','the_geom','shape_area','shape_len','fecha']]
    df_viviendas = df_viviendas.groupby(['Anyo','codigo_distrito', 'codigo_barrio'])['total_viviendas'].sum()
    df_viviendas.to_csv('../procesado/viviendas.csv', index=True)
    print("Listo!\n")

def generate_dataset_for_carto():
    df_autonomos = pd.read_csv('datos/procesado/autonomos.csv')
    df_migracion = pd.read_csv('datos/procesado/migracion.csv')
    df_parados = pd.read_csv('datos/procesado/parados.csv')
    df_poblacion = pd.read_csv('datos/procesado/poblacion.csv')
    df_renta = pd.read_csv('datos/procesado/renta.csv')
    df_viviendas = pd.read_csv('datos/procesado/viviendas.csv')
    df_hogar = pd.read_csv('datos/procesado/tamanyo_hogar.csv')
    df_incidentes = pd.read_csv('datos/procesado/incidentes.csv')
    df_venta = pd.read_csv('datos/procesado/precios_venta_historico.csv')
    df_alquiler = pd.read_csv('datos/procesado/precios_alquiler_historico.csv')
    df_bar1 = pd.read_csv('datos/raw/barrios.csv', decimal=',', delimiter=';',header=0).rename(columns={'COD_BAR':'codigo_barrio','BARRIO_MAY':'nombre_barrio','AREA':'area_barrio_m2'})
    df_bar2 = pd.read_csv('datos/raw/barrios-2.csv', decimal=',', delimiter=',',header=0).rename(columns={'codbar':'codigo_barrio','the_geom':'geom'})[['codigo_barrio','geom']]

    df_barrios = pd.merge(df_bar1, df_bar2, on='codigo_barrio')
    df_distritos = pd.read_csv('datos/raw/distritos.csv').rename(columns={'coddistrit':'codigo_distrito','nombre':'nombre_distrito'})[['codigo_distrito','nombre_distrito']]

    df_final = pd.merge(df_autonomos, df_incidentes, on=['codigo_distrito','Anyo'], how='outer')
    df_final = pd.merge(df_final, df_migracion, on=['codigo_distrito','Anyo','codigo_barrio'], how='outer')
    df_final = pd.merge(df_final, df_parados, on=['codigo_distrito','Anyo','codigo_barrio'], how='outer')
    df_final = pd.merge(df_final, df_poblacion, on=['codigo_distrito','Anyo','codigo_barrio'], how='outer')
    df_final = pd.merge(df_final, df_renta, on=['codigo_distrito','Anyo','codigo_barrio'], how='outer')
    df_final = pd.merge(df_final, df_viviendas, on=['codigo_distrito','Anyo','codigo_barrio'], how='outer')
    df_final = pd.merge(df_final, df_hogar, on=['codigo_distrito','Anyo','codigo_barrio'], how='outer')
    df_final = pd.merge(df_final, df_venta, on=['codigo_distrito','Anyo'], how='outer')
    df_final = pd.merge(df_final, df_alquiler, on=['codigo_distrito','Anyo'], how='outer')
    df_final = pd.merge(df_final, df_distritos, on='codigo_distrito')

    df_final = pd.merge(df_final, df_barrios, on='codigo_barrio')[['Anyo','codigo_barrio','nombre_barrio','area_barrio_m2','codigo_distrito','nombre_distrito','total_viviendas','tasa_extranjeros','parados','poblacion','renta','tamanyo_hogar','incidentes_por_distrito','autonomos','precio_venta_m2','precio_alquiler_m2','geom']]
    df_final['fecha'] = pd.to_datetime(dict(year=df_final['Anyo'], month=1, day=1))
    df_final.to_csv('datos/carto/kpis.csv', index=False)
    df_final[['Anyo','codigo_barrio','nombre_barrio','area_barrio_m2','codigo_distrito','nombre_distrito','total_viviendas','tasa_extranjeros','parados','poblacion','renta','tamanyo_hogar','incidentes_por_distrito','autonomos','precio_venta_m2','precio_alquiler_m2']].to_csv('datos/procesado/kpis_for_ML.csv', index=False)

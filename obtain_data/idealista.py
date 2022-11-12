import requests
import bs4 as bs
import pandas as pd
import numpy as np
import os
import requests

cookies = {
    'didomi_token': 'eyJ1c2VyX2lkIjoiMTg0MmFjZTgtNmI2YS02YTdkLTg1NDItYTdmYzI4N2ZkZGVmIiwiY3JlYXRlZCI6IjIwMjItMTAtMzBUMjE6MzE6MzAuNDU4WiIsInVwZGF0ZWQiOiIyMDIyLTEwLTMwVDIxOjMxOjMwLjQ1OFoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpsaW5rZWRpbi1tYXJrZXRpbmctc29sdXRpb25zIiwiYzptaXhwYW5lbCIsImM6YWJ0YXN0eS1MTGtFQ0NqOCIsImM6aG90amFyIiwiYzp5YW5kZXhtZXRyaWNzIiwiYzpiZWFtZXItSDd0cjdIaXgiLCJjOmFwcHNmbHllci1HVVZQTHBZWSIsImM6dGVhbGl1bWNvLURWRENkOFpQIiwiYzppZGVhbGlzdGEtTHp0QmVxRTMiLCJjOmlkZWFsaXN0YS1mZVJFamUyYyJdfSwicHVycG9zZXMiOnsiZW5hYmxlZCI6WyJhbmFseXRpY3MtSHBCSnJySzciLCJnZW9sb2NhdGlvbl9kYXRhIl19LCJ2ZXJzaW9uIjoyLCJhYyI6IkFGbUFDQUZrLkFBQUEifQ==',
    'euconsent-v2': 'CPhqXEAPhqXEAAHABBENCmCoAP_AAAAAAAAAF5wBAAIAAtAC2AvMAAABAaADAAEEiiUAGAAIJFFIAMAAQSKIQAYAAgkUOgAwABBIoJABgACCRQyADAAEEihUAGAAIJFA.f_gAAAAAAAAA',
    'datadome': '.Gm0CzhzPfMRJn6eFGMtppfl2nJE96J5Pde513SOWfg2WcjUTw5FJDsUYE5f62fbMo6daNL.uTb45ds_I6_kK2R~eetbTLt.UG4NDZ7zVl6Ba.Y_RQliN3DotW1LRfq.',
}

headers = {
    'authority': 'www.idealista.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'es-ES,es;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://www.idealista.com/sala-de-prensa/informes-precio-vivienda/venta/madrid-comunidad/madrid-provincia/madrid/arganzuela/',
    'sec-ch-device-memory': '8',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-full-version-list': '"Google Chrome";v="107.0.5304.62", "Chromium";v="107.0.5304.62", "Not=A?Brand";v="24.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}
distritos = ['Centro','Arganzuela','Retiro','Salamanca','Chamartin','Tetuan','Chamberi','Fuencarral','Moncloa','Latina','Carabanchel','Usera','Puente de Vallecas','Moratalaz','Ciudad Lineal','Hortaleza','Villaverde','Villa de Vallecas','Vicalvaro','San Blas','Barajas']
tipos = ['venta','alquiler']

def import_historico_idealista():
    for tipo in tipos:
        codigo_distrito = 0
        df_final = pd.DataFrame()
        for distrito in distritos:
            codigo_distrito += 1
            print('Obteniendo datos de {} del distrito: {}...'.format(tipo,distrito))
            url = 'https://www.idealista.com/sala-de-prensa/informes-precio-vivienda/{}/madrid-comunidad/madrid-provincia/madrid/{}/historico/'.format(tipo,distrito.lower().replace(' ','-'))
            response = requests.get(url, cookies=cookies, headers=headers)
            df = pd.read_html(response.text)[0]
            df = df.rename(columns={'Precio m2':'precio_{}_m2'.format(tipo),'Mes':'fecha_entrada'})
            df = df.loc[df['precio_{}_m2'.format(tipo)] != 'n.d.']
            df['precio_{}_m2'.format(tipo)] = [x.replace('.', '').replace(' €/m2','').replace(',','.') for x in df['precio_{}_m2'.format(tipo)]]
            df['precio_{}_m2'.format(tipo)] = df['precio_{}_m2'.format(tipo)].astype(float)
            df['Mes'] = df['fecha_entrada'].str.extract(r'([a-zA-Z]+)')
            df = df.replace({'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4, 'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8, 'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12})
            df['Anyo'] = df['fecha_entrada'].str.extract(r'(\d{4})')
            df['fecha'] = pd.to_datetime(dict(year=df['Anyo'], month=df['Mes'], day=1))
            df['codigo_distrito'] = codigo_distrito
            df[['fecha','precio_{}_m2'.format(tipo),'Anyo','codigo_distrito']].to_csv('datos/raw/precios_{}_historico/{}.csv'.format(tipo,distrito), index=False)
            df_final = df_final.append(df[['fecha','precio_{}_m2'.format(tipo),'Anyo','codigo_distrito']])
            print('Listo!')
        df_final = df_final.groupby(['Anyo','codigo_distrito'])['precio_{}_m2'.format(tipo)].mean()
        df_final.to_csv('datos/procesado/precios_{}_historico.csv'.format(tipo), index=True)





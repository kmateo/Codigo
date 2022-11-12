import pandas as pd
import numpy as np
from sklearn import preprocessing, cluster
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

def plot_elbow(sse, ks):
    fig, axis = plt.subplots(figsize=(9, 6))
    axis.set_title('Elbow method for optimal k')
    axis.set_xlabel('k')
    axis.set_ylabel('SSE')
    plt.plot(ks, sse, marker='o')
    plt.tight_layout()
    plt.show()


def plot_silhouette(sils, ks):
    fig, axis = plt.subplots(figsize=(9, 6))
    axis.set_title('Silhouette method')
    axis.set_xlabel('k')
    axis.set_ylabel('Silhouette')
    plt.plot(ks, sils, marker='o')
    plt.tight_layout()
    plt.show()


def elbow_method(data):
    sse = []
    ks = range(2, 10)
    for k in ks:
        k_means_model = cluster.KMeans(n_clusters=k, random_state=55)
        k_means_model.fit(data)
        sse.append(k_means_model.inertia_)
    plot_elbow(sse, ks)


def silhouette_method(data):
    ks = range(2, 10)
    sils = []
    for k in ks:
        clusterer = KMeans(n_clusters=k, random_state=55)
        cluster_labels = clusterer.fit_predict(data)
        silhouette_avg = silhouette_score(data, cluster_labels)
        sils.append(silhouette_avg)
        print("For n_clusters =", k, "The average silhouette_score is :",
              silhouette_avg)
    plot_silhouette(sils, ks)


def apply_kmeans():
    # 1 Filter rows from 2010 and 2021 to calculate differences
    dataset = pd.read_csv('datos/procesado/kpis_for_ML.csv')
    df = dataset[dataset['Anyo'].isin([2010, 2021])]

    # set 2010 values as negative and sum to calculate differences
    kpis = ['incidentes_por_distrito', 'tasa_extranjeros',
            'parados', 'autonomos','tamanyo_hogar',
            'precio_alquiler_m2', 'precio_venta_m2', 'renta']
    for kpi in kpis:
        df[kpi] = np.where(df['Anyo'] == 2010, -1 * df[kpi], df[kpi])

    df = (
        df
        .groupby(['codigo_barrio', 'nombre_barrio'])
        .agg(incidentes_por_distrito=('incidentes_por_distrito', sum),
                tasa_extranjeros=('tasa_extranjeros', sum),
                parados=(
                    'parados',
                    sum),
                autonomos=('autonomos',sum),
                tamanyo_hogar=(
                    'tamanyo_hogar', sum),
                precio_alquiler_m2=('precio_alquiler_m2', sum),
                precio_venta_m2=('precio_venta_m2', sum),
                renta=('renta', sum))
        .reset_index()
    )
    for kpi in kpis:
        df[kpi] = np.round(df[kpi], 2)

    # 2 Normalize
    df2 = df.copy()
    df2 = df2.drop(columns=['codigo_barrio', 'nombre_barrio'])
    x = df2.values  # returns a numpy array
    scaler = preprocessing.StandardScaler()
    x_scaled = scaler.fit_transform(x)
    df2 = pd.DataFrame(x_scaled)

    # 3 Correlations
    corr_matrix = df2.corr()
    corr_matrix = np.round(corr_matrix, 2)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, fmt="g", cmap='viridis', ax=ax,
                xticklabels=kpis, yticklabels=kpis)
    plt.tight_layout()
    fig.show()

    # Remove highly correlated variables
    df2 = df2.drop(columns=[1])

    # try PCA
    pca = PCA(n_components=6)
    pca.fit(df2)
    print(f'Variancia explicada PCA: {pca.explained_variance_ratio_}')

    # Optimal k
    silhouette_method(df2)
    elbow_method(df2)
    # elbow 5 - silhouette 6 -> 6

    # kmeans with k=5
    clusterer = KMeans(n_clusters=5, random_state=55)
    cluster_labels = clusterer.fit_predict(df2)
    df['cluster_k5'] = cluster_labels
    k5 = df[['codigo_barrio', 'nombre_barrio', 'cluster_k5']]
    dataset_k5 = pd.merge(dataset, k5, on=['codigo_barrio', 'nombre_barrio'])
    dataset_k5 = (
        dataset_k5
        .groupby(['Anyo', 'cluster_k5'])
        .agg(incidentes_por_distrito=('incidentes_por_distrito', 'mean'),
                tasa_extranjeros=('tasa_extranjeros', 'mean'),
                parados=(
                    'parados', 'mean'),
                autonomos=('autonomos', 'mean'),
                tamanyo_hogar=(
                    'tamanyo_hogar', 'mean'),
                precio_alquiler_m2=('precio_alquiler_m2', 'mean'),
                precio_venta_m2=('precio_venta_m2', 'mean'),
                renta=('renta', 'mean'))
        .reset_index()
    )
    dataset_k5.to_csv('datos/procesado/dataset_clusters_5.csv', index=False)

    # kmeans with k=6
    clusterer = KMeans(n_clusters=6, random_state=55)
    cluster_labels = clusterer.fit_predict(df2)
    df['cluster_k6'] = cluster_labels
    df['cluster_k6'] = df['cluster_k6']
    df_cluster = df[['codigo_barrio', 'nombre_barrio', 'cluster_k5', 'cluster_k6']]
    df_cluster.to_csv('datos/procesado/kmeans_clusters.csv', index=False)

    k6 = df[['codigo_barrio', 'nombre_barrio', 'cluster_k6']]
    dataset_k6 = pd.merge(dataset, k6, on=['codigo_barrio', 'nombre_barrio'])
    dataset_k6 = (
        dataset_k6
        .groupby(['Anyo', 'cluster_k6'])
        .agg(incidentes_por_distrito=('incidentes_por_distrito', 'mean'),
                tasa_extranjeros=('tasa_extranjeros', 'mean'),
                parados=(
                    'parados', 'mean'),
                autonomos=('autonomos', 'mean'),
                tamanyo_hogar=(
                    'tamanyo_hogar', 'mean'),
                precio_alquiler_m2=('precio_alquiler_m2', 'mean'),
                precio_venta_m2=('precio_venta_m2', 'mean'),
                renta=('renta', 'mean'))
        .reset_index()
    )
    dataset_k6.to_csv('datos/procesado/dataset_clusters_6.csv', index=False)

    df_bar1 = pd.read_csv('datos/raw/barrios.csv', decimal=',', delimiter=';',header=0).rename(columns={'COD_BAR':'codigo_barrio','BARRIO_MAY':'nombre_barrio','AREA':'area_barrio_m2'})
    df_bar2 = pd.read_csv('datos/raw/barrios-2.csv', decimal=',', delimiter=',',header=0).rename(columns={'codbar':'codigo_barrio','the_geom':'geom'})[['codigo_barrio','geom']]
    df_barrios = pd.merge(df_bar1, df_bar2, on='codigo_barrio')[['codigo_barrio','nombre_barrio','geom']]

    clusters_for_carto = pd.merge(df_cluster, df_barrios, on=['codigo_barrio', 'nombre_barrio'])
    clusters_for_carto.to_csv('datos/carto/clusters_carto.csv')

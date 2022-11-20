import pandas as pd
import numpy as np
import math
# Se crea estas funcines para hacer un poco más limpio el código
# Función para hallar la similitud entre dos usuarios


def similitudUsuarios(usuarioRecomendar, usuario):
    distancia = np.array((usuarioRecomendar-usuario)**2, dtype=float)
    return sum(distancia[~np.isnan(distancia)])**0.5


def similitudMaker(row, usuarioRow):
    return similitudUsuarios(usuarioRow.values[0][1:], row.values[1:])
# Weighted rating matrix


def weightMatrix(datasetFuncion):
    return datasetFuncion.iloc[:, 1:-1].multiply(datasetFuncion["Similitud"], axis="index")

# Weight sum


def weightSumFunction(weighted, normal):
    weightSum = {}
    for pelicula in weighted.columns:
        weightSum[pelicula] = sum(
            normal[~normal[pelicula].isna()]["Similitud"])
    return weightSum

# Función para identificar peliculas no calificadas


def peliculasNoCalificadasFuncion(usuarioFuncion):
    peliculasNoCalificadas = []
    for pelicula in usuarioFuncion.columns[1:]:
        if math.isnan(usuarioFuncion[pelicula].values[0]):
            peliculasNoCalificadas.append(pelicula)
    return peliculasNoCalificadas
# Función principal


def recomendar(datasetSelectBox, usuario, caso):
    # ¿Estamos usando los usuarios que creó el usuario o que creamos nosotros?
    if caso == "User-Made":
        peliculasDisponibles = pd.read_csv("Recursos/Consulta/Consulta.csv")
        peliculas = list(sorted(list(peliculasDisponibles["Titulo"])))
        dataset = pd.DataFrame(columns=["Usuario"]+peliculas)
        for usuario in datasetSelectBox:
            datAppend = {"Usuario": usuario}
            for pelicula in datasetSelectBox[usuario]:
                datAppend[pelicula] = datasetSelectBox[usuario][pelicula]
            dataset = dataset.append(datAppend, ignore_index=True)
    else:
        dataset = pd.read_csv("Recursos/Usuarios.csv")
    # Borrar columnas totalmente vacías
    dataset.dropna(how='all', axis=1, inplace=True)
    # Seleccionamos la fila del usuario
    rowUsuario = dataset.loc[dataset["Usuario"] == usuario]
    # Borrar la fila del dataset
    dataset.drop(dataset[dataset["Usuario"] == usuario].index, inplace=True)
    dataset.reset_index(inplace=True)
    dataset.drop('index', axis=1, inplace=True)
    # Ahora se debe de utilizar el algoritmo de recomendaciones como tal
    dataset["Similitud"] = dataset.apply(
        lambda row: similitudMaker(row, rowUsuario), axis=1)
    datasetWeight = weightMatrix(dataset)
    sumWeightRating = {pelicula: sum(np.array(datasetWeight[pelicula], dtype=float)[~np.isnan(
        np.array(datasetWeight[pelicula], dtype=float))]) for pelicula in datasetWeight.columns}
    weightSumValue = weightSumFunction(datasetWeight, dataset)
    resultados = {pelicula: round(
        sumWeightRating[pelicula]/weightSumValue[pelicula], 2) for pelicula in sumWeightRating}
    peliculasNocalificadas = peliculasNoCalificadasFuncion(rowUsuario)
    diccionarioPeliculasNoCalificadas = {
        pelicula: resultados[pelicula] for pelicula in peliculasNocalificadas}
    ordenPeliculasNoCalificadas = {pelicula: score for pelicula, score in sorted(
        diccionarioPeliculasNoCalificadas.items(), key=lambda item: item[1], reverse=True)[:5]}
    return pd.DataFrame({"Peliculas": [valor for valor in ordenPeliculasNoCalificadas], "Rating": [ordenPeliculasNoCalificadas[pelicula] for pelicula in ordenPeliculasNoCalificadas]})

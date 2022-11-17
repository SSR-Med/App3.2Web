import numpy as np
import pandas as pd
import random
# Vamos a leer el dataset de las peliculas
peliculas = pd.read_csv("Consulta/Consulta.csv")
titulos = list(peliculas["Titulo"])
data = {}
# Le vamos a poner nombre a los usuarios
data["Usuario"] = ["Usuario"+str(i) for i in range(300)]
# Vamos a crear 300 usuarios, donde cada usuario tiene un 60% de haber visto la pelicula, un 40% de que no la haya visto (estamos suponiendo que estos usuarios aman el cine)
for pelicula in titulos:
    data[pelicula] = [random.randint(0, 10) if random.random(
    ) <= 0.6 else float('nan') for i in range(300)]
Usuarios = pd.DataFrame(data)
Usuarios.to_csv("Usuarios.csv", index=False)

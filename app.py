import streamlit.components.v1 as html
from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import numpy as np
import json
import recomendacionColaborativa

# Se va a importar el dataset de usuarios hechos por nosotros (randomizados)
usuariosApp = pd.read_csv("Recursos/Usuarios.csv")
# Todos los usuarios y calificaciones de peliculas hechos desde la aplicación por los mismos clientes
with open('Recursos/madeUsers.json', 'r') as fp:
    usuarios = json.load(fp)
# Se va a importar el dataset de las peliculas
peliculasDisponibles = pd.read_csv("Recursos/Consulta/Consulta.csv")
# Los nombres de todas las peliculas
peliculas = tuple(sorted(list(peliculasDisponibles["Titulo"])))
# El menú
with st.sidebar:
    choose = option_menu(
        "Menú", ["Creación usuarios", "Usuario y recomendaciones", "Reiniciar usuarios"], icons=["clipboard-data", "diagram-2", "backspace"], menu_icon="app-indicator", default_index=0,
        styles={
            "container": {"padding": "5!important"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#02ab21"}, })
# Para crear los usuarios
if choose == "Creación usuarios":
    st.title("Creación de los usuarios")
    nombreUsuario = st.text_input('Nombre del usuario')
    pelicula = st.selectbox('Elige la película a calificar', peliculas)
    CalificacionPelicula = st.slider(
        "¿Qué calificación le pones a esta película?", 0, 10, 0)
    if st.button("Insertar calificación"):
        if nombreUsuario not in usuarios:
            usuarios[nombreUsuario] = {}
        usuarios[nombreUsuario][pelicula] = CalificacionPelicula
        open('Recursos/madeUsers.json', 'w').close()
        st.write(str(usuarios))
        with open('Recursos/madeUsers.json', 'w') as fp:
            json.dump(usuarios, fp)
elif choose == "Reiniciar usuarios":
    st.title("Reiniciar usuarios")
    st.write("Advertencia: Esta acción reinicia todos los usuarios que previamente ha creado, ¿está seguro de que desea continuar?")
    if st.button("Reiniciar"):
        open('Recursos/madeUsers.json', 'w').close()
        with open('Recursos/madeUsers.json', 'w') as fp:
            json.dump({}, fp)
elif choose == "Usuario y recomendaciones":
    st.title("Recomendaciones al usuario")
    st.write(
        "Para que funcione correctamente el programa se deben de seguir estas condiciones:")
    st.markdown("1. Elegir el dataset en el cual se encuentra el usuario.")
    st.markdown("1.1 User-Made: La que realizó en Creación Usuarios.")
    st.markdown(
        "1.2 App-Based: La que viene por defecto en nuestra app (Usuario0-Usuario299)")
    st.markdown("2. Seleccionar el nombre de usuario")
    st.markdown("3. Darle al botón. ")
    st.write("La salida del programa van a ser las 5 películas recomendadas según el usuario seleccionado (pueden llegar a ser menos, esto pasaría en el caso de que sean pocas las películas que el usuario no ha visto)")
    datasetsDisponibles = st.selectbox(
        "Elige el dataset", ("User-Made", "App-Based"))
    if datasetsDisponibles == "User-Made":
        nombresUsuariosDataset = [usuario for usuario in usuarios]
    else:
        nombresUsuariosDataset = list(usuariosApp["Usuario"])
    usuariosBox = st.selectbox(
        "Elige el usuario con el que vas a trabajar", nombresUsuariosDataset)
    if st.button("Recomendaciones"):
        dataFrameResultado = recomendacionColaborativa.recomendar(
            usuarios, usuariosBox, datasetsDisponibles)
        st.dataframe(dataFrameResultado)

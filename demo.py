import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import numpy as np
import plotly_express as px
import random

from urllib.error import URLError

st.set_page_config(page_title= "Proyecto Titanic - Milagros Vidal - Upgrade",
                   page_icon = 	"🧊",
                   layout="wide")

try:
    df = pd.read_csv("titanic.csv")
    
    video_file = open('/Users/milagrosvidal/Documents/GitHub/ProyectoTitanic/Titanicgoodluck.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    st.title(":ship: 🧊Titanic")
    st.subheader("Bootcamp Data Analytics by Upgrade")
    st.markdown("##")
    
    st.sidebar.header("Índice")
    
    st.write("### Datos crudos", df)
    st.title("Valores nulos de las columnas")
        
    # Paso 1: Qué columnas tienen valores nulos?

    valores_nulos = df.isnull().sum().reset_index()
    valores_nulos.columns = ['Columnas', 'Número de Valores Nulos']
    valores_nulos['Porcentaje nulos'] = ((valores_nulos["Número de Valores Nulos"] / len(df)) * 100).round(2)
    st.write("Calcular el número de valores nulos por columna", valores_nulos.sort_values(by="Número de Valores Nulos", ascending=False))

    # Paso 2: Cálculo del porcentaje de filas con atributos nulos
    def calcular_porcentaje_filas_nulas(df):
        total_filas = len(df)
        filas_con_nulos = df.isnull().any(axis=1).sum()
        porcentaje_nulos = (filas_con_nulos / total_filas) * 100
        return porcentaje_nulos
        
    
    porcentaje_nulos = calcular_porcentaje_filas_nulas(df)
    st.write(f"Porcentaje de filas con al menos un valor nulo: {porcentaje_nulos:.2f}%")

    
    st.write("Cabin 77.10% valores nulos")
    st.write("Age 19.87% valores nulos")
    st.write("Embarked 0.22% valores nulos")
        


    st.write("### Tratamiento de columnas con valores nulos: Cabin, Age, Embarked:")
    st.write("#### Tratamiento de valores nulos col Age, con la mediana")
    st.write("##### ¿Por qué con la mediana?: debido a su capacidad para manejar valores atípicos y representar mejor el centro en distribuciones asimétricas.")



#         # data = data.T.reset_index()
#         # data = pd.melt(data, id_vars=["index"]).rename(
#         #     columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
#         # )
#         # chart = (
#         #     alt.Chart(data)
#         #     .mark_area(opacity=0.3)
#         #     .encode(
#         #         x="year:T",
#         #         y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
#         #         color="Region:N",
#         #     )
#         # )
#         # st.altair_chart(chart, use_container_width=True)
except URLError as e:
     st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )
    
    ##### Valores nulos:
###### Age 19.87% valores nulos
###### Cabin 77.10% valores nulos - Voy a indicar en otra columna si esta presente la info o no, para no eliminar la info. de la columna
###### Embarked 0.22% valores nulos
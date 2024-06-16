import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import numpy as np
import plotly_express as px
import random
import plotly.graph_objects as go
import statistics

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

    valores_nulos_original = df.isnull().sum().reset_index()
    valores_nulos_original.columns = ['Columnas', 'Número de Valores Nulos']
    valores_nulos_original['Porcentaje nulos'] = ((valores_nulos_original["Número de Valores Nulos"] / len(df)) * 100).round(2)
    st.write("Calcular el número de valores nulos por columna", valores_nulos_original.sort_values(by="Número de Valores Nulos", ascending=False))

    # Paso 2: Cálculo del porcentaje de filas con atributos nulos
    def calcular_porcentaje_filas_nulas(df):
        total_filas = len(df)
        filas_con_nulos = df.isnull().any(axis=1).sum()
        porcentaje_nulos = (filas_con_nulos / total_filas) * 100
        return porcentaje_nulos
        
    
    porcentaje_nulos = calcular_porcentaje_filas_nulas(df)
    st.write(f"Porcentaje de filas con al menos un valor nulo: {porcentaje_nulos:.2f}%")

    porcentajes_nulos = {
    "Cabin": 77.10,
    "Age": 19.87,
    "Embarked": 0.22
    }

# Indicadores de Progreso
    st.write("### Indicadores de Valores Nulos")
    for columna, porcentaje in porcentajes_nulos.items():
        st.write(f"{columna}: {porcentaje}%")
        st.progress(porcentaje / 100)

     # Tarjetas informativas usando st.metric
    st.write("### Tarjetas Informativas")
    col1, col2, col3 = st.columns(3)
    col1.metric("Cabin", f"{porcentajes_nulos['Cabin']}%", delta=None)
    col2.metric("Age", f"{porcentajes_nulos['Age']}%", delta=None)
    col3.metric("Embarked", f"{porcentajes_nulos['Embarked']}%", delta=None)

# Calcular el número de valores nulos por columna
    valores_nulos = df.isnull().sum().reset_index()
    valores_nulos.columns = ['Columnas', 'Número de Valores Nulos']

# Definir colores personalizados para las barras
    colores = ['#1f77b4' if col == 'Age' else '#9467bd' if col == 'Cabin' else '#2ca02c' for col in valores_nulos['Columnas']]

# Crear el gráfico de barras interactivo
    data_nulos = px.bar(
        valores_nulos,
        x='Columnas',
        y='Número de Valores Nulos',
        title='Número de Valores Nulos por Columna',
        labels={'Número de Valores Nulos': 'Número de Valores Nulos', 'Columnas': 'Columnas'},
        text='Número de Valores Nulos',
        template='plotly_white'
    )

    # Personalizar el diseño del gráfico
    data_nulos.update_traces(textposition='outside', marker=dict(color=colores, line=dict(color='black', width=1.5)))
    data_nulos.update_layout(
        width=800,  # Ajustar ancho del gráfico
        height=600,  # Ajustar altura del gráfico
        xaxis_tickangle=-45,
        title_font_size=20,
        title_font_family='Arial',
        title_font_color='black',
        font=dict(size=14, family='Arial', color='black'),
        plot_bgcolor='lightgrey',  # Color de fondo del gráfico
        paper_bgcolor='lightgrey',  # Color de fondo del papel
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='gray')
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(data_nulos)

    st.write("### Tratamiento de columnas con valores nulos: Cabin, Age, Embarked:")
    st.write("#### Tratamiento de valores nulos col Age, con la mediana")
    st.write("###### ¿Por qué con la mediana?: debido a su capacidad para manejar valores atípicos y representar mejor el centro en distribuciones asimétricas.")
    
    # Tratamiento de valores nulos col "Age", con la mediana.

    median_age = df['Age'].median()
    df['Age'].fillna(median_age, inplace=True)

    st.write(f"La edad mediana es: {median_age:.2f}")
    
    

    # Crear un gráfico de dispersión de todas las edades
    fig = px.scatter(df, x=df.index, y='Age', title='Edades de los pasajeros del Titanic')

    # Añadir una línea horizontal que marque la mediana
    fig.add_trace(go.Scatter(
        x=[0, len(df)],  # Extender la línea a lo largo del gráfico
        y=[median_age, median_age],  # Ambas y-coordinates son la mediana de la edad
        mode='lines',  # Dibujar una línea
        name=f'Mediana: {median_age:.2f}',  # Nombre de la línea
        line=dict(color='yellow', dash='dash')  # Color rojo y línea discontinua
    ))


    # Añadir un slider para filtrar edades y hacer el gráfico más interactivo
    min_age, max_age = st.slider('Selecciona el rango de edad:', int(df['Age'].min()), int(df['Age'].max()), (int(df['Age'].min()), int(df['Age'].max())))
    st.write(f"La edad máxima y mínima es de {min_age} a {max_age} años")
    # Filtrar el DataFrame según el rango de edad seleccionado
    df_filtered = df[(df['Age'] >= min_age) & (df['Age'] <= max_age)]

    # Actualizar el gráfico con los datos filtrados
    fig_filtered = px.scatter(df_filtered, x=df_filtered.index, y='Age', title='Edades de los pasajeros del Titanic',
                            labels={'index': 'Pasajero', 'Age': 'Edad'})

    fig_filtered.add_trace(go.Scatter(
        x=[0, len(df) - 1],  # Extender la línea a lo largo del gráfico
        y=[median_age, median_age],  # Ambas y-coordinates son la mediana de la edad
        mode='lines',  # Dibujar una línea
        name=f'Mediana: {median_age:.2f}',  # Nombre de la línea
        line=dict(color='red', dash='dash')  # Color rojo y línea discontinua
    ))

    # Mostrar el gráfico filtrado en Streamlit
    st.plotly_chart(fig_filtered)
    
    st.write("#### Tratamiento de valores nulos col Embarked, con la moda")
    st.write("###### ¿Por qué con la moda?: Al no ser un dato númerico, se busca la categoria que más se repite.")
    
    # Calcular la moda de la columna "Embarked"
    moda_embarked_corregido = df['Embarked'].mode()[0]
    
    df["Embarked"].fillna(moda_embarked_corregido, inplace=True)
    nulos_embarked = df["Embarked"].isnull().sum()
    
    st.write("#### Tratamiento de valores nulos col Cabin")
    st.write("###### ")
    
    # Tratamiento de la columna Cabin: crear otra para indicar que hay info o no.

    # Crear una nueva columna indicadora de la presencia de datos en 'Cabin'
        # Update the 'Cabin' column to replace NaN values with 'Unknown'
    df['Cabin'] = df['Cabin'].fillna('Unknown')
    
    # Create a new indicator column for the presence of data in 'Cabin'
    df['Cabin_Ind'] = df['Cabin'] != 'Unknown'
    
    # Verify there are no null values in the 'Cabin' column
    null_values_after = df['Cabin'].isnull().sum()
    
    st.write(df[['Cabin_Ind']])
   

# Recalcular los valores nulos después del tratamiento
    valores_nulos_actualizados = df.isnull().sum().reset_index()
    valores_nulos_actualizados.columns = ['Columnas', 'Número de Valores Nulos']
    valores_nulos_actualizados['Porcentaje nulos'] = ((valores_nulos_actualizados["Número de Valores Nulos"] / len(df)) * 100).round(2)

    # Recalcular el porcentaje de filas con atributos nulos después del tratamiento
    porcentaje_nulos_actualizados = calcular_porcentaje_filas_nulas(df)

# Porcentajes de valores nulos en las columnas específicas después del tratamiento
    porcentajes_nulos_actualizados = {
    "Cabin": valores_nulos_actualizados[valores_nulos_actualizados['Columnas'] == 'Cabin_Ind']['Porcentaje nulos'].values[0],
    "Age": valores_nulos_actualizados[valores_nulos_actualizados['Columnas'] == 'Age']['Porcentaje nulos'].values[0],
    "Embarked": valores_nulos_actualizados[valores_nulos_actualizados['Columnas'] == 'Embarked']['Porcentaje nulos'].values[0]
}
    st.subheader('Porcentaje de valores nulos después del tratamiento')
    col1, col2, col3 = st.columns(3)
    
    col1.metric(label="Cabin", value=f"{porcentajes_nulos_actualizados['Cabin']:.2f}%")
    col2.metric(label="Age", value=f"{porcentajes_nulos_actualizados['Age']:.2f}%")
    col3.metric(label="Embarked", value=f"{porcentajes_nulos_actualizados['Embarked']:.2f}%")

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
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
                   layout="wide")
st.sidebar.header("Índice")
indice_items = [
    "Datos crudos",
    "Valores nulos",
    "Número de pasajeros embarcados",
    "Distribución de sexos",
    "Supuestos"
]

selected_item = st.sidebar.selectbox("Selecciona una sección:", indice_items)

try:
    df = pd.read_csv("titanic.csv")
    
    video_file = open('/Users/milagrosvidal/Documents/GitHub/ProyectoTitanic/Titanicgoodluck.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
    st.write("Eso es todo entonces. Adíos videojuegos, adíos bañarse. Buena suerte compañeros 🥲")
    
    
    st.title(":ship: 🧊Titanic")
    st.subheader("Bootcamp Data Analytics by Upgrade")
    st.markdown("##")
    
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

    # Diseño del gráfico
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

    # Mostrar el gráfico
    st.plotly_chart(data_nulos)

    st.write("### Tratamiento de columnas con valores nulos: Cabin, Age, Embarked:")
    st.write("#### Tratamiento de valores nulos col Age, con la mediana")
    st.write("###### ¿Por qué con la mediana?: debido a su capacidad para manejar valores atípicos y representar mejor el centro en distribuciones asimétricas.")
    
    
                                                    #### VALORES NULOS AGE ####
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

    # Añadir un slider para filtrar edades
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

    # Mostrar el gráfico filtrado
    st.plotly_chart(fig_filtered)
    
                                                    #### VALORES NULOS EMBARKED ####
    
    st.write("#### Tratamiento de valores nulos col Embarked, con la moda")
    # Texto estilizado con efectos
    st.markdown("""
        <style>
        .typewriter-text {
            font-size: 22px;
            font-weight: bold;
            font-family: 'Courier New', Courier, monospace;
            color: #ffffff;
            background: linear-gradient(90deg, #e0c3fc, #8ec5fc);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            color: transparent;
            animation: typewriter 4s steps(44) 1s 1 normal both, shimmer 5s linear infinite;
            border-right: 2px solid rgba(255, 255, 255, 0.75);
            padding-right: 5px;
        }

        @keyframes typewriter {
            from { width: 0; }
            to { width: 100%; }
        }

        @keyframes shimmer {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }
        </style>

        <div class="typewriter-text">
            ¿Por qué con la moda?: Al no ser un dato númerico, se busca la categoria que más se repite.
        </div>
    """, unsafe_allow_html=True)

    # Calcular la moda de la columna "Embarked"
    moda_embarked_corregido = df['Embarked'].mode()[0]
    
    df["Embarked"].fillna(moda_embarked_corregido, inplace=True)
    nulos_embarked = df["Embarked"].isnull().sum()
    
    st.write("#### Tratamiento de valores nulos col Cabin")
    st.write("###### ")
    
    # Tratamiento de la columna Cabin: crear otra para indicar que hay info o no.
    df['Cabin'] = df['Cabin'].fillna('Unknown')
    
    # Otra columna que indique los valores nulos
    df['Cabin_Ind'] = df['Cabin'] != 'Unknown'
    
    # Chequeo que se hayan corregido los valores nulos
    null_values_after = df['Cabin'].isnull().sum()
    
    st.write(df[['Cabin_Ind']])

    # Recalcular los valores nulos después del tratamiento
    valores_nulos_actualizados = df.isnull().sum().reset_index()
    valores_nulos_actualizados.columns = ['Columnas', 'Número de Valores Nulos']
    valores_nulos_actualizados['Porcentaje nulos'] = ((valores_nulos_actualizados["Número de Valores Nulos"] / len(df)) * 100).round(2)

    # Recalcular el porcentaje de filas con atributos nulos después del tratamiento
    porcentaje_nulos_actualizados = calcular_porcentaje_filas_nulas(df)

    # Porcentajes de valores nulos en las columnas cabin,age y embarked después del tratamiento
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
    
    
    st.subheader('Precios más bajos y más altos en las tarifas')
    lowest_fare = df['Fare'].round(0).astype(int).min()
    highest_fare = df['Fare'].round(0).astype(int).max()    
    

    # Línea animada
    st.markdown("""
        <style>
        @keyframes wave {
            0% { transform: translateY(0); }
            20% { transform: translateY(-10px); }
            40% { transform: translateY(10px); }
            60% { transform: translateY(-10px); }
            80% { transform: translateY(10px); }
            100% { transform: translateY(0); }
        }

        .animated-line {
            width: 100%;
            height: 5px;
            background: linear-gradient(90deg, #ff7e5f, #feb47b, #86A8E7, #91EAE4, #ff7e5f);
            background-size: 200% 200%;
            animation: gradient 6s ease infinite, wave 2s infinite;
            margin: 20px 0;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        </style>
        <div class="animated-line"></div>
        """, unsafe_allow_html=True)

# Calcular los precios más bajos y más altos
    lowest_fare = df['Fare'].round(0).astype(int).min()
    highest_fare = df['Fare'].round(0).astype(int).max()

    st.markdown(f"""
    <style>
    .card {{
        background-color: #4CAF50;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        transition: transform 0.3s;
        margin: 10px;
    }}
    .card:hover {{
        transform: scale(1.05);
    }}
    .card-high {{
        background-color: #FF5733;
    }}
    </style>

    <div style="display: flex; justify-content: center; gap: 20px;">
        <div class="card">
            <h2>Precio más bajo pagado</h2>
            <p style="font-size: 36px;">${lowest_fare}</p>
        </div>
        <div class="card card-high">
            <h2>Precio más alto pagado</h2>
            <p style="font-size: 36px;">${highest_fare}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Botón para mostrar información adicional y reproducir audio
    if st.button('Mostrar detalles'):
        st.markdown(f"""
            <div style="text-align: center; font-size: 18px; margin-top: 20px;">
                <p>El precio más bajo pagado fue ${lowest_fare}, que es significativamente menor que el precio más alto pagado de ${highest_fare}. Esto muestra una gran variabilidad en las tarifas. Hoy $512, equivalen aprox $49.000.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.title("Número de pasajeros embarcados")
        # Calcular el número de pasajeros embarcados
    num_pasajeros = len(df)
    st.write(f"El número de pasajeros embarcados es: {num_pasajeros}")
    
    st.title("Distribución de sexo de personas embarcadas")

    # Obtener la distribución de sexos y renombrar etiquetas
    sex_distribucion = df['Sex'].value_counts().reset_index()
    sex_distribucion.columns = ['Sexo', 'Cantidad de pasajeros']
    sex_distribucion['Sexo'] = sex_distribucion['Sexo'].replace({'male': 'Hombre', 'female': 'Mujer'})

    # Color pickers para seleccionar colores
    col1, col2 = st.columns(2)

    with col1:
        color_mujer = st.color_picker('Selecciona el color para Mujer', '#FF69B4')

    with col2:
        color_hombre = st.color_picker('Selecciona el color para Hombre', '#1E90FF')

    # Crear un diccionario de colores basados en las selecciones
    color_map = {'Mujer': color_mujer, 'Hombre': color_hombre}

    # Crear gráfico de pastel interactivo con Plotly
    fig = px.pie(sex_distribucion, values='Cantidad de pasajeros', names='Sexo',
                title='Distribución de Sexos de Personas Embarcadas en el Titanic',
                color='Sexo', color_discrete_map=color_map)

    # mostrar porcentajes
    fig.update_traces(textinfo='percent+label', hoverinfo='label+percent+value')

    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig)

    # Calcular el número total de sobrevivientes (donde 'Survived' es 1)
    total_survivors = df[df['Survived'] == 1].shape[0]
    st.write(f"El número de total de sobrevivientes: {total_survivors}")
    
    # Filtrar el DataFrame para obtener solo los sobrevivientes
    survivors_df = df[df['Survived'] == 1]

    # Contar el número de sobrevivientes por sexo
    survivors_by_sex = survivors_df['Sex'].value_counts()

    # Reemplazar 'female' por 'mujeres' y 'male' por 'hombres'
    survivors_by_sex.index = survivors_by_sex.index.map({'female': 'mujeres', 'male': 'hombres'})

    # Calcular el porcentaje de sobrevivientes por sexo
    total_survivors = survivors_by_sex.sum()
    percentages_by_sex = (survivors_by_sex / total_survivors) * 100

    # Mostrar los números de sobrevivientes
    mujeres_sobrevivientes = survivors_by_sex.get('mujeres', 0)
    hombres_sobrevivientes = survivors_by_sex.get('hombres', 0)
    st.write(f"El número de sobrevivientes por sexo: Mujer {mujeres_sobrevivientes} y Hombre {hombres_sobrevivientes}")

    # Crear el gráfico de pastel con tamaño reducido
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.pie(percentages_by_sex, labels=percentages_by_sex.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff'])
    ax.set_title('Porcentaje de sobrevivientes por sexo')

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)


    st.header("Supuestos para el análisis de Titanic")
    supuestos = [
        "1. La mayoría de los pasajeros de primera clase sobrevivieron.",
        "2. Las mujeres y niños tuvieron mayores tasas de supervivencia.",
        "3. La tarifa del billete está correlacionada con la probabilidad de supervivencia.",
        "4. Los pasajeros de mayor edad tenían menor probabilidad de sobrevivir.",
        "5. Sobrevivieron los hombres que pagaron más por su boleto.",
        "6. El hombre que más pagó sobrevivió ante la mujer que menos pagó."
    ]

    for supuesto in supuestos:
        st.write(supuesto)

    st.write("### Selecciona un supuesto para visualizar los datos correspondientes:")
    selected_supuesto = st.selectbox("Supuestos:", supuestos)

    if selected_supuesto == "1. La mayoría de los pasajeros de primera clase sobrevivieron.":
        survival_by_class = df.groupby('Pclass')['Survived'].mean() * 100
        total_by_class = df['Pclass'].value_counts(normalize=True) * 100
        fig, ax = plt.subplots()
        bars = ax.bar(survival_by_class.index, survival_by_class.values)
        ax.set_title('Supervivencia por clase')
        ax.set_xlabel('Clase')
        ax.set_ylabel('Porcentaje de sobrevivientes')
        ax.bar_label(bars, fmt='%.1f%%')
        st.pyplot(fig)
        conclusion = "La mayoría de los pasajeros de primera clase no sobrevivieron." if survival_by_class.loc[1] < 50 else "La mayoría de los pasajeros de primera clase sobrevivieron."
        explanation = f"La tasa de supervivencia de los pasajeros de primera clase es del {survival_by_class.loc[1]:.2f}%."
        st.write(conclusion)
        st.write(explanation)

    elif selected_supuesto == "2. Las mujeres y niños tuvieron mayores tasas de supervivencia.":
        df['Child'] = df['Age'] < 18
        survival_by_sex_age = df.groupby(['Sex', 'Child'])['Survived'].mean().unstack().fillna(0) * 100
        survival_by_sex_age.index = ['Hombres', 'Mujeres']
        survival_by_sex_age.columns = ['Adultos', 'Niños']
        fig, ax = plt.subplots()
        survival_by_sex_age.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Supervivencia por sexo y edad')
        ax.set_xlabel('Sexo')
        ax.set_ylabel('Tasa de supervivencia (%)')
        for container in ax.containers:
            ax.bar_label(container, fmt='%.1f%%')
        st.pyplot(fig)
        
        women_survival_rate = survival_by_sex_age.loc['Mujeres'].mean()
        children_survival_rate = survival_by_sex_age.loc[:, 'Niños'].mean()
        men_survival_rate = survival_by_sex_age.loc['Hombres', 'Adultos']
        
        if women_survival_rate > men_survival_rate and children_survival_rate > men_survival_rate:
            conclusion = "Las mujeres y los niños tuvieron mayores tasas de supervivencia."
            explanation = (f"La tasa de supervivencia de las mujeres es del {women_survival_rate:.2f}%, "
                        f"y la de los niños es del {children_survival_rate:.2f}%, ambos mayores que la de los hombres adultos que es del {men_survival_rate:.2f}%.")
        else:
            conclusion = "Las mujeres y los niños no tuvieron mayores tasas de supervivencia."
            explanation = (f"La tasa de supervivencia de las mujeres es del {women_survival_rate:.2f}%, "
                        f"y la de los niños es del {children_survival_rate:.2f}%, pero no superan la de los hombres adultos que es del {men_survival_rate:.2f}%.")
        
        st.write(conclusion)
        st.write(explanation)

    
    elif selected_supuesto == "3. La tarifa del billete está correlacionada con la probabilidad de supervivencia.":
        correlation = df['Fare'].corr(df['Survived'])
        fig, ax = plt.subplots()
        sns.regplot(x='Fare', y='Survived', data=df, logistic=True, ci=None, scatter_kws={'alpha':0.5}, line_kws={'color':'red'}, ax=ax)
        ax.set_title('Tarifa del billete vs Supervivencia')
        ax.set_xlabel('Tarifa del billete')
        ax.set_ylabel('Supervivencia (0 = No, 1 = Sí)')
        st.pyplot(fig)
        
        conclusion = "Existe una correlación positiva entre la tarifa del billete y la probabilidad de supervivencia."
        explanation = f"La correlación entre la tarifa del billete y la probabilidad de supervivencia es de {correlation:.2f}. "\
                    "Esto significa que, en general, los pasajeros que pagaron tarifas más altas tenían una mayor probabilidad de sobrevivir. "\
                    "Esto puede deberse a varios factores:\n"\
                    "1. **Clase Socioeconómica**: Los pasajeros de primera clase, que pagaron tarifas más altas, tenían un mejor acceso a los botes salvavidas.\n"\
                    "2. **Ubicación en el Barco**: Los camarotes de primera clase estaban en los niveles superiores, más cerca de los botes salvavidas.\n"\
                    "3. **Atención y Rescate Prioritario**: Hubo una prioridad para rescatar a los pasajeros de mayor estatus social primero."
        
        st.write(conclusion)
        st.write(explanation)

    elif selected_supuesto == "4. Los pasajeros de mayor edad tenían menor probabilidad de sobrevivir.":
        correlation = df['Age'].corr(df['Survived'])
        fig, ax = plt.subplots()
        hist = ax.hist([df[df['Survived'] == 1]['Age'].dropna(), df[df['Survived'] == 0]['Age'].dropna()], 
                    bins=10, label=['Sobrevivieron', 'No sobrevivieron'])
        ax.set_title('Distribución de edad y supervivencia')
        ax.set_xlabel('Edad')
        ax.set_ylabel('Número de pasajeros')
        ax.legend()
        st.pyplot(fig)
        conclusion = "Los pasajeros de mayor edad tenían menor probabilidad de sobrevivir." if correlation < 0 else "No hay una correlación significativa entre la edad y la probabilidad de supervivencia."
        explanation = f"La correlación entre la edad y la probabilidad de supervivencia es de {correlation:.2f}. "\
                    "Esto significa que, en general, a medida que la edad aumenta, la probabilidad de supervivencia tiende a disminuir ligeramente, pero la relación no es fuerte. "\
                    "En otras palabras, la edad de un pasajero pudo tener muy poca influencia sobre su probabilidad de supervivencia en el Titanic."
        
        st.write(conclusion)
        st.write(explanation)

    elif selected_supuesto == "5. Sobrevivieron los hombres que pagaron más por su boleto.":
        male_fare_survival = df[df['Sex'] == 'male'].groupby('Survived')['Fare'].mean()
        fig, ax = plt.subplots()
        bars = ax.bar(male_fare_survival.index, male_fare_survival.values, tick_label=['No sobrevivieron', 'Sobrevivieron'])
        ax.set_title('Tarifa media pagada por los hombres según supervivencia')
        ax.set_xlabel('Supervivencia')
        ax.set_ylabel('Tarifa media')
        ax.bar_label(bars, fmt='%.2f')
        st.pyplot(fig)
        conclusion = "Los hombres que pagaron más por su boleto tenían mayor probabilidad de sobrevivir." if male_fare_survival.loc[1] > male_fare_survival.loc[0] else "No hay una correlación significativa entre la tarifa pagada y la supervivencia de los hombres."
        explanation = f"La tarifa media pagada por los hombres que sobrevivieron es de {male_fare_survival.loc[1]:.2f}, comparada con {male_fare_survival.loc[0]:.2f} de los que no sobrevivieron."
        st.write(conclusion)
        st.write(explanation)

    elif selected_supuesto == "6. El hombre que más pagó sobrevivió ante la mujer que menos pagó.":
        max_fare_male = df[df['Sex'] == 'male']['Fare'].max()
        min_fare_female = df[df['Sex'] == 'female']['Fare'].min()
        
        max_fare_male_survived = df[(df['Sex'] == 'male') & (df['Fare'] == max_fare_male)]['Survived'].values[0]
        min_fare_female_survived = df[(df['Sex'] == 'female') & (df['Fare'] == min_fare_female)]['Survived'].values[0]
        
        conclusion_male = "El hombre que más pagó sobrevivió." if max_fare_male_survived == 1 else "El hombre que más pagó no sobrevivió."
        conclusion_female = "La mujer que menos pagó sobrevivió." if min_fare_female_survived == 1 else "La mujer que menos pagó no sobrevivió."
        
        st.write(f"El hombre que más pagó: {conclusion_male}")
        st.write(f"La mujer que menos pagó: {conclusion_female}")
        
        if max_fare_male_survived == 1 and min_fare_female_survived == 0:
            conclusion = "El hombre que más pagó sobrevivió ante la mujer que menos pagó."
            explanation = (f"El hombre que pagó más ({max_fare_male:.2f}) sobrevivió, mientras que "
                        f"la mujer que pagó menos ({min_fare_female:.2f}) no sobrevivió.")
        else:
            conclusion = "El hombre que más pagó no sobrevivió ante la mujer que menos pagó."
            explanation = (f"El hombre que pagó más ({max_fare_male:.2f}) no sobrevivió, mientras que "
                        f"la mujer que pagó menos ({min_fare_female:.2f}) sí sobrevivió.")
        
        st.write(conclusion)
        st.write(explanation)
    
except URLError as e:
     st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )
    
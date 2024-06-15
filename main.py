import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import requests
import seaborn as sns

titanicorignal = pd.read_csv("titanic.csv")
titanicorignal

df = pd.read_csv("/Users/milagrosvidal/Documents/GitHub/ProyectoTitanic/titanic.csv")
df

df.info()

df.head()

##### Valores nulos:
###### Age 19.87% valores nulos
###### Cabin 77.10% valores nulos - Voy a indicar en otra columna si esta presente la info o no, para no eliminar la info. de la columna
###### Embarked 0.22% valores nulos


#### Valores nulos

cabin_data = df["Cabin"]
cabin_data

df.describe()

import plotly.express as px

# Calcular el número de valores nulos por columna
valores_nulos = df.isnull().sum().reset_index()
valores_nulos.columns = ['Columnas', 'Número de Valores Nulos']

# Definir colores personalizados para las barras
colores = ['#1f77b4' if col == 'Age' else '#9467bd' if col == 'Cabin' else '#2ca02c' for col in valores_nulos['Columnas']]

# Crear el gráfico de barras interactivo
fig = px.bar(
    valores_nulos,
    x='Columnas',
    y='Número de Valores Nulos',
    title='Número de Valores Nulos por Columna',
    labels={'Número de Valores Nulos': 'Número de Valores Nulos', 'Columnas': 'Columnas'},
    text='Número de Valores Nulos',
    template='plotly_white'
)

# Personalizar el diseño del gráfico
fig.update_traces(textposition='outside', marker=dict(color=colores, line=dict(color='black', width=1.5)))
fig.update_layout(
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
fig.show()

# Tratamiento de la columna Cabin: crear otra para indicar que hay info o no.

# Crear una nueva columna indicadora de la presencia de datos en 'Cabin'
df['Cabin_Ind'] = df['Cabin'].apply(lambda x: 0 if pd.isnull(x) else 1)

# Mostrar las primeras filas del DataFrame para verificar la nueva columna
df.head()

# Calcular el número total de sobrevivientes (donde 'Survived' es 1)
total_survivors = df[df['Survived'] == 1].shape[0]

# Mostrar el resultado
print(f"Total de sobrevivientes: {total_survivors}")

# Filtrar los datos para obtener solo las filas donde 'Survived' es 1
survivors = df[df['Survived'] == 1]

# Contar el número de sobrevivientes por sexo
survivors_by_sex = survivors['Sex'].value_counts()

# Mostrar el resultado
print(survivors_by_sex)

# Suponiendo que ya tienes cargado el DataFrame `titanic_data`

# Filtrar los datos para obtener solo las filas donde la columna 'Cabin' no es nula
df_con_cabina = df[df['Cabin'].notna()]

# Contar cuántas personas con cabina sobrevivieron
survivors_con_cabina = df_con_cabina[df_con_cabina['Survived'] == 1].shape[0]

# Mostrar el resultado
print(f"Cantidad de personas con cabina que sobrevivieron: {survivors_con_cabina}")

# Contar cuántas personas con cabina sobrevivieron por sexo
survivors_con_cabina_by_sex = df_con_cabina[df_con_cabina['Survived'] == 1].groupby('Sex').size()

# Mostrar el resultado
print("Cantidad de personas con cabina que sobrevivieron por sexo:")
print(survivors_con_cabina_by_sex)

# Filtrar los datos para obtener solo las filas donde la columna 'Cabin' es nula
df_sin_cabina = df[df['Cabin'].isna()]

# Contar cuántas personas sin cabina sobrevivieron
survivors_sin_cabina = df_sin_cabina[df_sin_cabina['Survived'] == 1].shape[0]

# Mostrar el resultado
print(f"Cantidad de personas sin cabina que sobrevivieron: {survivors_sin_cabina}")

# Filtrar los datos para obtener solo las filas donde la columna 'Cabin' no es nula
df_con_cabina = df[df['Cabin'].notna()]

# Filtrar los datos para obtener solo las filas donde la columna 'Cabin' es nula
df_sin_cabina = df[df['Cabin'].isna()]

# Estadísticas descriptivas de las tarifas pagadas por pasajeros con cabina
fare_con_cabina_stats = df_con_cabina['Fare'].describe()
print("Tarifas pagadas por pasajeros con cabina:")
print(fare_con_cabina_stats)

# Estadísticas descriptivas de las tarifas pagadas por pasajeros sin cabina
fare_sin_cabina_stats = df_sin_cabina['Fare'].describe()
print("\nTarifas pagadas por pasajeros sin cabina:")
print(fare_sin_cabina_stats)

# Visualización
plt.figure(figsize=(12, 6))

# Distribución de tarifas para pasajeros con cabina
sns.histplot(df_con_cabina['Fare'], kde=True, color='blue', label='Con Cabina')

# Distribución de tarifas para pasajeros sin cabina
sns.histplot(df_sin_cabina['Fare'], kde=True, color='red', label='Sin Cabina')

plt.title('Distribución de Tarifas Pagadas: Con Cabina vs Sin Cabina')
plt.xlabel('Tarifa')
plt.ylabel('Frecuencia')
plt.legend()
plt.show()

#### Valores nulos Age

# Tratamiento de valores nulos col "Age", con la mediana.

median_age = df['Age'].median()
df['Age'].fillna(median_age, inplace=True)

median_age
print(f"La edad promedio es: {median_age} años")

#Corroborar que quedó sin valores nulos la col "Age"

checknulos_age = df['Age'].isnull().sum()
checknulos_age

#### Valores Nulos "Embarked"

# Tratamiento de valores nulos col "Embarked", con la moda al no ser un dato númerico.
# Calculo de la moda de la colum "Embarked" con statistics
import statistics
moda_embarked = df["Embarked"]
moda = statistics.mode(moda_embarked)
moda

df["Embarked"].fillna(moda_embarked, inplace=True)
nulos_embarked = df["Embarked"].isnull().sum()
nulos_embarked

#### Precios más altos y más bajos

# Calcular los precios más bajos y más altos
lowest_fare = df['Fare'].round(0).astype(int).min()
highest_fare = df['Fare'].round(0).astype(int).max()

lowest_fare, highest_fare
print(f"Valor más bajo: ${lowest_fare}")
print(f"Valor más alto: ${highest_fare}")

# Quién pagó más?
person_highest_fare = df[df['Fare'].round(0).astype(int) == highest_fare]

# Obtener el valor de la columna 'Sex' y 'Survived'
sex_of_person = person_highest_fare['Sex'].values[0]
survived_status = person_highest_fare['Survived'].values[0]

# Convertir el estado de sobrevivencia a texto
survived_text = "sobrevivió" if survived_status == 1 else "no sobrevivió"

print(f"La persona que pagó el precio más alto es: {sex_of_person} y {survived_text}")

# Quién pagó más?
person_lowest_fare = df[df['Fare'].round(0).astype(int) == lowest_fare]

# Obtener el valor de la columna 'Sex' y 'Survived'
sex_of_person = person_lowest_fare['Sex'].values[0]
survived_status = person_lowest_fare['Survived'].values[0]

# Convertir el estado de sobrevivencia a texto
survived_text = "sobrevivió" if survived_status == 1 else "no sobrevivió"

print(f"La persona que pagó el precio más bajo es: {sex_of_person} y {survived_text}")

#### El hombre que más pagó, sobrevivió?

# Redonde la columna 'Fare' y encuentra el valor máximo para 'male'
highest_fare_male = df[df['Sex'] == 'male']['Fare'].round(0).astype(int).max()
highest_fare_male

# Encontrar la fila correspondiente al precio más alto para 'male'
male_highest_fare = df[(df['Sex'] == 'male') & (df['Fare'].round(0).astype(int) == highest_fare_male)]


# Obtener el valor de la columna 'Survived' para 'male' que pagó más
survived_status_male = male_highest_fare['Survived'].values[0]

# Convertir el estado de sobrevivencia a texto
survived_text_male = "sobrevivió" if survived_status_male == 1 else "no sobrevivió"


print(f"El hombre que más pagó la tarifa fue de ${highest_fare_male} y {survived_text_male} ")

#### El hombre que menos pagó, sobrevivió?

# Redondea la columna 'Fare' y encuentra el valor máximo para 'male'
lowest_fare_male = df[df['Sex'] == 'male']['Fare'].round(0).astype(int).min()
lowest_fare_male

# Encontrar la fila correspondiente al precio más alto para 'male'
male_lowest_fare = df[(df['Sex'] == 'male') & (df['Fare'].round(0).astype(int) == lowest_fare_male)]


# Obtener el valor de la columna 'Survived' para 'male' que pagó más
survived_status_male = male_lowest_fare ['Survived'].values[0]

# Convertir el estado de sobrevivencia a texto
survived_text_male = "sobrevivió" if survived_status_male == 1 else "no sobrevivió"


print(f"El hombre que menos pagó la tarifa fue de ${lowest_fare_male} y {survived_text_male} ")

#### Conclusión de este punto:
###### Quizas haya sido un tripulante que lo catalogaron como pasajero y por eso no pagó nada. Esto podría explicar que no haya sobrevivido porque no era prioridad rescatarlo. También puede deber a algún error de carga, invitados por la empresa, etc.

#### Distribución de sexos embarcados

# Crear un gráfico de pastel para la distribución de sexos 
fig, ax = plt.subplots(figsize=(4, 4))
sex_distribucion = df['Sex'].value_counts()
wedges, texts, autotexts = ax.pie(sex_distribucion, colors=['#48D1CC', '#7B68EE'], autopct='%1.1f%%', startangle=140)

# Agregar leyenda
ax.legend(wedges, ['Mujer', 'Hombre'], title="Sexo", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), frameon=False)

plt.title('Distribución de Sexos de Personas Embarcadas en el Titanic')
plt.axis('equal')
plt.show()
import pandas as pd
from google.colab import files

uploaded = files.upload()

archivo_excel = 'Mental health Depression disorder Data.xlsx'

try:
    # Leer todas las hojas
    hojas = pd.read_excel(archivo_excel, sheet_name=None)
    print("Hojas en el archivo:", hojas.keys())

    # Comprobar acceso a una hoja
    hoja1 = hojas['prevalence-of-depression-males-']
    print(hoja1.head())
except FileNotFoundError:
    print(f"Error: No se encontró el archivo {archivo_excel}")
    print("Asegúrate de subir el archivo y que el nombre sea correcto.")

try:
    hojas = pd.read_excel(archivo_excel, sheet_name=None)
    print("Hojas originales en el archivo:", hojas.keys())

    # Lista de hojas a eliminar
    hojas_a_eliminar = ['prevalence-by-mental-and-substa',
                         'depression-by-level-of-educatio',
                         'prevalence-of-depression-by-age',
                         'suicide-rates-vs-prevalence-of-']

    # Eliminar hojas
    for hoja in hojas_a_eliminar:
        if hoja in hojas:
            del hojas[hoja]
            print(f"La hoja '{hoja}' ha sido eliminada.")
        else:
            print(f"La hoja '{hoja}' no existe en el archivo.")

    # Mostrar las hojas restantes
    print("\nHojas restantes:")
    for nombre_hoja, datos in hojas.items():
        print(f"\nPrimeras filas de la hoja '{nombre_hoja}':")
        print(datos.head())

except FileNotFoundError:
    print(f"Error: No se encontró el archivo {archivo_excel}")
    print("Asegúrate de subir el archivo y que el nombre sea correcto.")

try:
    hoja_especifica = 'prevalence-of-depression-males-'
    datos = pd.read_excel(archivo_excel, sheet_name=hoja_especifica)

    # Filtrar filas para México
    datos_filtrados = datos[datos['Entity'] == 'Mexico']

    print(f"Datos filtrados (solo 'Mexico'):\n{datos_filtrados.head()}")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo {archivo_excel}")
except FileNotFoundError:
    print(f"Error: No se encontró el archivo {archivo_excel}")

import pandas as pd
import numpy as np

def fusionar_datos_depresion(archivo_excel):
    try:
        prevalencia_males = pd.read_excel(archivo_excel, sheet_name='prevalence-of-depression-males-')
        numero_depresion = pd.read_excel(archivo_excel, sheet_name='number-with-depression-by-count')

        prevalencia_males['Year'] = pd.to_numeric(prevalencia_males['Year'], errors='coerce')
        numero_depresion['Year'] = pd.to_numeric(numero_depresion['Year'], errors='coerce')

        # Filtrar datos para México por rango de años
        prevalencia_males_filtrado = prevalencia_males[
            (prevalencia_males['Entity'] == 'Mexico') &
            (prevalencia_males['Year'] >= 1990) &
            (prevalencia_males['Year'] <= 2017)
        ]

        numero_depresion_filtrado = numero_depresion[
            (numero_depresion['Entity'] == 'Mexico') &
            (numero_depresion['Year'] >= 1990) &
            (numero_depresion['Year'] <= 2017)
        ]

        datos_fusionados = pd.merge(
            prevalencia_males_filtrado,
            numero_depresion_filtrado,
            on=['Entity', 'Year', 'Code'],
            suffixes=('_prevalencia', '_numero')
        )

        columnas_seleccionadas = [
            'Entity',
            'Code',
            'Year'
        ]

        for col in datos_fusionados.columns:
            if 'Prevalence in males (%)' in col:
                columnas_seleccionadas.append(col)
            if 'Prevalence in females (%)' in col:
                columnas_seleccionadas.append(col)
            if 'Population' in col:
                columnas_seleccionadas.append(col)
            if 'Number' in col:
                columnas_seleccionadas.append(col)

        # Crear dataframe final
        datos_finales = datos_fusionados[columnas_seleccionadas].copy()

        # Renombrar columnas
        nuevos_nombres = {
            'Entity': 'Entity',
            'Code': 'Code',
            'Year': 'Year'
        }

        for col in datos_finales.columns:
            if 'Prevalence (%)' in col:
                nuevos_nombres[col] = 'Prevalence in males (%)'
            elif 'Prevalence in females (%)' in col:
                nuevos_nombres[col] = 'Prevalence in females (%)'
            elif 'Number' in col:
                nuevos_nombres[col] = 'Depressive disorders (Number)'

        datos_finales = datos_finales.rename(columns=nuevos_nombres)

        # Ordenar por año
        datos_finales = datos_finales.sort_values('Year')

        # Archivo Excel
        nombre_archivo_salida = 'datos_limpiados.xlsx'
        with pd.ExcelWriter(nombre_archivo_salida) as writer:
            datos_finales.to_excel(writer, index=False, sheet_name='fusion')

        # Convertir el archivo final a CSV
        nombre_csv_salida = 'datos_limpiados.csv'
        datos_finales.to_csv(nombre_csv_salida, index=False)
        print(f"Archivo CSV guardado: {nombre_csv_salida}")

        print(f"\nArchivo guardado: {nombre_archivo_salida}")
        print(f"Total de registros: {len(datos_finales)}")
        print("\nColumnas finales:")
        print(datos_finales.columns.tolist())
        print("\nPrimeros registros:")
        print(datos_finales.head())

        return datos_finales

    except Exception as e:
        print(f"Error en el proceso: {e}")
        return None

archivo_excel = 'Mental health Depression disorder Data.xlsx'
resultado = fusionar_datos_depresion(archivo_excel)

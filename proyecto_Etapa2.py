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

import pandas as pd
import numpy as np

def fusionar_datos_depresion(archivo_excel):
    try:
        prevalencia_males = pd.read_excel(archivo_excel, sheet_name='prevalence-of-depression-males-')
        numero_depresion = pd.read_excel(archivo_excel, sheet_name='number-with-depression-by-count')

        prevalencia_males['Year'] = pd.to_numeric(prevalencia_males['Year'], errors='coerce')
        numero_depresion['Year'] = pd.to_numeric(numero_depresion['Year'], errors='coerce')

        # Listado de países
        paises_filtrados = [
            "Australia", "Brazil", "Canada", "Chile", "China", "Colombia", "France",
            "Germany", "Guatemala", "Italy", "Japan", "Mexico", "Netherlands",
            "Russia", "South Korea", "Spain", "Switzerland", "United States"
        ]

        # Filtrado de datos
        prevalencia_males_filtrado = prevalencia_males[
            (prevalencia_males['Entity'].isin(paises_filtrados)) &
            (prevalencia_males['Year'] >= 1990) &
            (prevalencia_males['Year'] <= 2017)
        ]

        numero_depresion_filtrado = numero_depresion[
            (numero_depresion['Entity'].isin(paises_filtrados)) &
            (numero_depresion['Year'] >= 1990) &
            (numero_depresion['Year'] <= 2017)
        ]

        datos_fusionados = pd.merge(
            prevalencia_males_filtrado.drop(columns=['Code'], errors='ignore'),
            numero_depresion_filtrado.drop(columns=['Code'], errors='ignore'),
            on=['Entity', 'Year'],
            suffixes=('_prevalencia', '_numero')
        )

        columnas_seleccionadas = ['Entity', 'Year']

        for col in datos_fusionados.columns:
            if 'Prevalence in males (%)' in col or 'Prevalence in females (%)' in col or 'Population' in col or 'Number' in col:
                columnas_seleccionadas.append(col)

        # Dataframe final
        datos_finales = datos_fusionados[columnas_seleccionadas].copy()

        # Renombrar columnas
        nuevos_nombres = {
            'Entity': 'Entity',
            'Year': 'Year'
        }

        for col in datos_finales.columns:
            if 'Prevalence in males (%)' in col:
                nuevos_nombres[col] = 'Prevalence in males (%)'
            elif 'Prevalence in females (%)' in col:
                nuevos_nombres[col] = 'Prevalence in females (%)'
            elif 'Number' in col:
                nuevos_nombres[col] = 'Depressive disorders (Number)'

        datos_finales = datos_finales.rename(columns=nuevos_nombres)

        # Total (%)
        if 'Depressive disorders (Number)' in datos_finales.columns and 'Population' in datos_finales.columns:
            datos_finales['Total (%)'] = (datos_finales['Depressive disorders (Number)'] / datos_finales['Population']) * 100

        # Ordenar por año
        datos_finales = datos_finales.sort_values('Year')

        # Guardar en Excel
        nombre_archivo_salida = 'datos_limpiadosII.xlsx'
        with pd.ExcelWriter(nombre_archivo_salida) as writer:
            datos_finales.to_excel(writer, index=False, sheet_name='fusion')

        # Guardar en CSV
        nombre_csv_salida = 'datos_limpiadosII.csv'
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

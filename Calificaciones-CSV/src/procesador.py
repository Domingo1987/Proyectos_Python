import os
import csv
import pandas as pd
from datetime import datetime

class ProcesadorCSV:
    def __init__(self, tipo_por_defecto, fecha_por_defecto, fechas_bloqueadas=None):
        self.tipo_por_defecto = tipo_por_defecto
        self.fecha_por_defecto = fecha_por_defecto
        self.external_id_counter = 1  # Contador global para el External ID
        # Lista de fechas que se deben excluir
        self.fechas_bloqueadas = fechas_bloqueadas if fechas_bloqueadas else []



    def procesar_archivos(self, archivo_input_path, carpeta_output):
        if not os.path.exists(carpeta_output):
            os.makedirs(carpeta_output)

        try:
            # Leer el archivo de entrada y ordenarlo por 'ID de usuario único'
            df = pd.read_csv(archivo_input_path)
            df.sort_values(by='ID de usuario único', inplace=True)

            # Procesar y generar archivos de salida
            self.generar_archivos_salida(df, carpeta_output)
        except PermissionError as e:
            print(f"Error de permisos al intentar leer el archivo: {e}")
        except Exception as e:
            print(f"Ocurrió un error al procesar los archivos: {e}")

    def generar_archivos_salida(self, df, carpeta_output):
        for user_id, group in df.groupby('ID de usuario único'):
            archivo_output_path = os.path.join(carpeta_output, f"{user_id}.csv")
            datos_formateados = self.formatear_datos(group)
            # Ordenar los datos formateados por fecha
            datos_formateados = sorted(datos_formateados, key=lambda x: x['fecha'])
            
            with open(archivo_output_path, mode='w', newline='') as archivo_output:
                campos = ['External ID','fecha', 'nota', 'tipo']
                escritor = csv.DictWriter(archivo_output, fieldnames=campos)
                escritor.writeheader()
                escritor.writerows(datos_formateados)

    def formatear_datos(self, group):
        datos_formateados = []
        for index, row in group.iterrows():
            external_id = self.external_id_counter  # Usar el contador global para el External ID
            self.external_id_counter += 1  # Incrementar el contador global
            
            puntos_max = row.get('Puntos máximos', '')   
            fecha_raw = row.get('Fecha límite de la tarea', '')
            
            # Obtener la fecha formateada
            if pd.isna(fecha_raw) or fecha_raw == '':
                fecha = self.fecha_por_defecto
            else:
                fecha = self.formatear_fecha(fecha_raw)
            
            # Si la fecha está en la lista de fechas bloqueadas, omitir esta fila
            if fecha in self.fechas_bloqueadas:
                continue

            nota_id = row.get('Calificación', '1')
            if pd.isna(nota_id) or nota_id in ['', 'Faltante']:
                nota_id = 1
            else:
                try:
                    nota_id = round((float(nota_id) / puntos_max) * 12)
                except ValueError:
                    nota_id = 1
            tipo = self.tipo_por_defecto
            if 'Foro' in row.get('Título de la tarea', ''):
                tipo = 'Oral'

            datos_formateados.append({
                'External ID': external_id,
                'fecha': fecha,
                'nota': nota_id,
                'tipo': tipo
            })

        return datos_formateados

    def formatear_fecha(self, fecha):
        try:
            # Intentar convertir la fecha al formato YYYY-MM-DD
            fecha_formateada = datetime.strptime(fecha, "%d/%m/%y %I:%M%p").strftime("%Y-%m-%d")
        except ValueError:
            fecha_formateada = self.fecha_por_defecto
        return fecha_formateada
    
    def generar_xls(self, archivo_input_path, archivo_output_path):
        df = pd.read_csv(archivo_input_path)
        df.sort_values(by='ID de usuario único', inplace=True)

        # Crear un nuevo DataFrame para el XLS
        xls_data = []

        # Campos base para el DataFrame
        base_columns = ['ID de usuario único', 'Nombre', 'Apellido']

        # Recopilar todas las combinaciones de tareas para los encabezados de columnas
        columnas_completas = set()
        for _, row in df.iterrows():
            combinacion_tarea = f"{row['Título de la tarea']}, {row['Fecha límite de la tarea']}, {row['Puntos máximos']}, {row['Categoría de calificación']}"
            columnas_completas.add(combinacion_tarea)
        
        columnas_completas = sorted(columnas_completas)  # Ordenar para mantener consistencia
        all_columns = base_columns + list(columnas_completas)

        # Crear un diccionario para cada usuario
        user_data = {}
        puntos_max = row.get('Puntos máximos', '')   

        
        for user_id, group in df.groupby('ID de usuario único'):
            nombre = group['Nombre'].iloc[0]
            apellido = group['Apellido'].iloc[0]
            user_info = {'ID de usuario único': user_id, 'Nombre': nombre, 'Apellido': apellido}

            for index, row in group.iterrows():
                combinacion_tarea = f"{row['Título de la tarea']}, {row['Fecha límite de la tarea']}, {row['Puntos máximos']}, {row['Categoría de calificación']}"
                calificacion = row['Calificación']
                if pd.isna(calificacion) or calificacion in ['', 'Faltante']:
                    calificacion = 1
                else:
                    try:
                        #nota_id = round(float(nota_id) / 2)
                        calificacion = round((float(calificacion) / puntos_max)*12)
                    except ValueError:
                        calificacion = 1
                
                user_info[combinacion_tarea] = calificacion
            
            user_data[user_id] = user_info

        # Convertir el diccionario en una lista de listas para el DataFrame
        for user_id, info in user_data.items():
            row_data = [info.get(col, '') for col in all_columns]
            xls_data.append(row_data)

        # Crear DataFrame y guardar en XLSX
        xls_df = pd.DataFrame(xls_data, columns=all_columns)
        xls_df.to_excel(archivo_output_path, index=False)

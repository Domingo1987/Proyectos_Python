import os
from src.procesador import ProcesadorCSV

def main():
    # Se puede modificar la fecha por defecto aquí
    tipo_por_defecto = "Trabajo"
    fecha_por_defecto = "2024-04-01"
    # Lista de fechas a bloquear
    fechas_bloqueadas = ["2024-05-06", "2024-05-21", "2024-05-29", "2024-08-17"]
    
    procesador = ProcesadorCSV(tipo_por_defecto, fecha_por_defecto, fechas_bloqueadas)
    
    

    # Ruta de los archivos CSV de entrada y salida
    carpeta_input = "input/"
    archivo_input = os.path.join(carpeta_input, "gradebook-export.csv")
    carpeta_output = "output/"

    # Lógica para procesar los archivos
    procesador.procesar_archivos(archivo_input, carpeta_output)
    
    # Generar el archivo XLS
    archivo_xls_output = os.path.join(carpeta_output, "resultado.xlsx")
    procesador.generar_xls(archivo_input, archivo_xls_output)

if __name__ == "__main__":
    main()
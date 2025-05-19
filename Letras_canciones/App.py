import requests
from bs4 import BeautifulSoup
import json
import os
import time
import random

class LetrasScraper:
    def __init__(self):
        self.base_url = "https://www.letras.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.data = {
            "artistas": [],
            "canciones": [],
            "ultima_actualizacion": None
        }
    
    def get_soup(self, url):
        """Obtiene el objeto BeautifulSoup de una URL con manejo de errores y demoras aleatorias"""
        try:
            # Esperar entre 1 y 3 segundos entre solicitudes para evitar ser bloqueado
            time.sleep(random.uniform(1, 3))
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Lanza excepción si hay error HTTP
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener la página {url}: {e}")
            return None
    
    def buscar_artista(self, nombre_artista):
        """Busca un artista y devuelve su URL"""
        # Primero intentamos una búsqueda directa formateando el nombre para la URL
        nombre_formateado = nombre_artista.lower().replace(' ', '-')
        direct_url = f"{self.base_url}/{nombre_formateado}/"
        
        # Verificamos si la URL directa existe
        response = requests.get(direct_url, headers=self.headers)
        if response.status_code == 200:
            return direct_url
        
        # Si no funciona la URL directa, usamos el buscador
        query = nombre_artista.replace(' ', '+')
        search_url = f"{self.base_url}/search/{query}"
        soup = self.get_soup(search_url)
        
        if not soup:
            return None
        
        resultados = soup.select('.gs-title a')
        for resultado in resultados:
            href = resultado.get('href', '')
            if '/artista/' in href or (self.base_url in href and '/' in href.replace(self.base_url, '')):
                return href
        
        return None
    
    def obtener_canciones_artista(self, url_artista):
        """Obtiene la lista completa de canciones de un artista con sus metadatos"""
        soup = self.get_soup(url_artista)
        if not soup:
            return []
            
        canciones = []
        
        # Buscamos las filas de la tabla de canciones
        filas_canciones = soup.select('li.songlist-table-row')
        
        for fila in filas_canciones:
            try:
                # Extraemos los atributos data-* que necesitamos
                data_id = fila.get('data-id', '')
                data_dns = fila.get('data-dns', '')
                data_url = fila.get('data-url', '')
                data_artist = fila.get('data-artist', '')
                data_name = fila.get('data-name', '')
                data_shareurl = fila.get('data-shareurl', '')
                data_sharetext = fila.get('data-sharetext', '')
                
                # Verificamos si hay una etiqueta a para la URL
                link_element = fila.select_one('a')
                url_cancion = link_element.get('href') if link_element else ''
                if url_cancion and not url_cancion.startswith('http'):
                    url_cancion = self.base_url + url_cancion
                
                # Verificamos si existe URL de significado
                url_significado = None
                if data_dns and data_url:
                    url_significado = f"{self.base_url}/{data_dns}/{data_url}/significado.html"
                
                cancion_info = {
                    "data_id": data_id,
                    "data_dns": data_dns,
                    "data_url": data_url,
                    "data_artist": data_artist,
                    "data_name": data_name,
                    "data_shareurl": data_shareurl,
                    "data_sharetext": data_sharetext,
                    "url_cancion": url_cancion,
                    "url_significado": url_significado
                }
                
                canciones.append(cancion_info)
            except Exception as e:
                print(f"Error al procesar una canción: {e}")
                continue
                
        return canciones
    
    def obtener_datos_artista(self, url_artista):
        """Obtiene datos generales de un artista y sus canciones con metadatos"""
        soup = self.get_soup(url_artista)
        if not soup:
            return None
        
        nombre = soup.select_one('h1.head')
        
        datos_artista = {
            "nombre": nombre.text.strip() if nombre else "Desconocido",
            "url": url_artista,
            "canciones": self.obtener_canciones_artista(url_artista)
        }
        
        return datos_artista
        
    def obtener_significados(self, url_significado):
        """Extrae el significado de una canción si está disponible"""
        soup = self.get_soup(url_significado)
        if not soup:
            return None
            
        significados = []
        
        # Buscar contenedores de significados
        contenedores = soup.select('div.cnt-letra p')
        for contenedor in contenedores:
            significados.append(contenedor.get_text().strip())
        
        return {
            "url": url_significado,
            "texto": "\n\n".join(significados) if significados else "No hay significados disponibles"
        }
    
    def buscar_por_genero(self, genero):
        """Busca artistas por género musical"""
        url_genero = f"{self.base_url}/generos/{genero}"
        soup = self.get_soup(url_genero)
        
        if not soup:
            return []
        
        artistas = []
        lista_artistas = soup.select('ul.cnt-list li a')
        
        for i, artista in enumerate(lista_artistas[:3]):  # Limitado a 3 artistas para no sobrecargar
            url_artista = artista.get('href')
            if url_artista and not url_artista.startswith('http'):
                url_artista = self.base_url + url_artista
                
            datos_artista = self.obtener_datos_artista(url_artista)
            if datos_artista:
                artistas.append(datos_artista)
                
        return artistas
    
    def guardar_datos(self, filename="letras_data.json"):
        """Guarda los datos recopilados en un archivo JSON"""
        import datetime
        self.data["ultima_actualizacion"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            print(f"Datos guardados exitosamente en {filename}")
            return True
        except Exception as e:
            print(f"Error al guardar los datos: {e}")
            return False

# Archivo App.py - Interfaz principal para el usuario
if __name__ == "__main__":
    scraper = LetrasScraper()

    print("=== Scraper de Letras.com ===")
    print("\n¿Qué acción desea realizar?")
    print("1. Buscar artista y extraer metadatos de canciones")
    print("2. Buscar artista y extraer significados de canciones")
    opcion = input("\nSeleccione una opción (1-2): ")
    
    if opcion == "1":
        nombre_artista = input("\nIngrese el nombre del artista: ")
        print(f"\nBuscando artista '{nombre_artista}'...")
        url_artista = scraper.buscar_artista(nombre_artista)
        
        if url_artista:
            print(f"Artista encontrado. URL: {url_artista}")
            print("Extrayendo datos y metadatos de canciones...")
            datos_artista = scraper.obtener_datos_artista(url_artista)
            print("Datos totales: ",len(datos_artista))
            print("Datos keys: ",datos_artista)
            
            if datos_artista and datos_artista["canciones"]:
                print(f"Se encontraron {len(datos_artista['canciones'])} canciones.")
                scraper.data["artistas"].append(datos_artista)
                scraper.data["canciones"].extend(datos_artista["canciones"])
                
                # Mostrar algunos metadatos de ejemplo
                if datos_artista["canciones"]:
                    print("\nEjemplo de metadatos extraídos (primera canción):")
                    cancion = datos_artista["canciones"][0]
                    print(f"  Nombre: {cancion['data_name']}")
                    print(f"  DNS: {cancion['data_dns']}")
                    print(f"  Share URL: {cancion['data_shareurl']}")
                    print(f"  URL significado: {cancion['url_significado']}")
            else:
                print("No se encontraron canciones para este artista.")
        else:
            print(f"No se encontró el artista '{nombre_artista}'.")
            
    elif opcion == "2":
        nombre_artista = input("\nIngrese el nombre del artista: ")
        print(f"\nBuscando artista '{nombre_artista}'...")
        url_artista = scraper.buscar_artista(nombre_artista)
        
        if url_artista:
            print(f"Artista encontrado. URL: {url_artista}")
            print("Extrayendo datos y significados de canciones...")
            datos_artista = scraper.obtener_datos_artista(url_artista)
            
            if datos_artista and datos_artista["canciones"]:
                print(f"Se encontraron {len(datos_artista['canciones'])} canciones.")
                
                # Extraer significados para las primeras 3 canciones como ejemplo
                canciones_con_significado = []
                for i, cancion in enumerate(datos_artista["canciones"][:3]):
                    if cancion["url_significado"]:
                        print(f"Extrayendo significado de '{cancion['data_name']}'...")
                        significado = scraper.obtener_significados(cancion["url_significado"])
                        if significado:
                            cancion["significado"] = significado
                            canciones_con_significado.append(cancion)
                
                scraper.data["canciones"].extend(canciones_con_significado)
                print(f"Se extrajeron significados para {len(canciones_con_significado)} canciones.")
            else:
                print("No se encontraron canciones para este artista.")
        else:
            print(f"No se encontró el artista '{nombre_artista}'.")
    
    else:
        print("Opción no válida.")
    
    # Guardar los datos recopilados
    if scraper.data["artistas"] or scraper.data["canciones"]:
        scraper.guardar_datos()
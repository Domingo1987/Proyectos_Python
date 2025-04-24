from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import IPython.display as ipd
import os
import sys

# Forzar UTF-8 si estás en Windows
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Cargar archivo .env
load_dotenv()

# Obtener la API Key desde .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validar que se haya cargado la clave
if not OPENAI_API_KEY:
    raise EnvironmentError("No se encontró la API key. Asegúrate de tener un archivo .env con OPENAI_API_KEY.")

# Inicializar cliente de OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Crear carpeta de salida si no existe
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# Texto breve
texto_breve = "Suscríbete al canal para apoyar la creación de contenido técnico."
salida_breve = output_dir / "breve.mp3"

# Generar audio
response = client.audio.speech.create(
    model='gpt-4o-mini-tts',
    voice='coral',
    input=texto_breve
)
response.stream_to_file(salida_breve)
print(f"[✓] Audio breve guardado en: {salida_breve}")

# Texto largo (fragmento de El Principito)
texto_largo = """El Objetivo de Desarrollo Sostenible 4 nos interpela con una meta ambiciosa: “Garantizar una educación inclusiva y equitativa de calidad y promover oportunidades de aprendizaje permanente para todos” (UNESCO, 2015, p. 7). En este marco, se despliegan metas concretas como asegurar la finalización de los niveles primario y secundario (meta 4.1), el acceso a la educación inicial (4.2), a la formación técnico-profesional y superior (4.3), el desarrollo de competencias para el empleo (4.4), la eliminación de disparidades de género y la atención a poblaciones vulnerables (4.5), la alfabetización (4.6) y la educación para el desarrollo sostenible (4.7).

Analizar estas metas desde la política educativa digital en Uruguay supone poner en tensión logros y desafíos. Tal como desarrolló María Teresa Lugo (2017) en su conferencia, el país se destaca por haber universalizado el acceso a dispositivos y conectividad a través del Plan Ceibal, configurándose como un faro en la región. Sin embargo, esa infraestructura no garantiza por sí sola transformaciones profundas. Lugo advierte que "la infraestructura muchas veces aparece como el árbol que tapa el bosque", en tanto es condición necesaria pero no suficiente para avanzar en inclusión y calidad educativa (Lugo, 2017).

La planificación con TIC requiere un enfoque sistémico. El Marco de Acción para el ODS 4 señala que “se deben desplegar todos los esfuerzos posibles para garantizar que, esta vez, se consigan el objetivo y las metas” (UNESCO, 2015, p. 22), y remarca la importancia de una gobernanza efectiva que respalde desde lo macro la concreción en lo micro (p. 57). Esto resuena con el planteo de Lugo sobre la necesidad de identificar “nudos críticos” que hoy siguen tensionando nuestras escuelas: ausentismo, brechas entre sectores, desvinculación en secundaria, baja pertinencia curricular, entre otros.

Desde esta mirada, la inclusión de tecnologías en la educación no puede ser una respuesta genérica. Como se planteó en clase, no se trata de “revolear soluciones tecnológicas”, sino de diseñar con claridad del propósito, desde una pedagogía situada. La tecnología debe ser entendida como “una aliada para pensar y contemplar condiciones de acceso y gestionar modelos pedagógicos situados y transformadores” (Lugo, 2017).

En Uruguay, aún con ventajas comparativas, persisten inequidades que comprometen el cumplimiento pleno del ODS 4. Las trayectorias educativas interrumpidas o debilitadas son un llamado a fortalecer los proyectos pedagógicos con sentido inclusivo, articulando conectividad efectiva, formación docente continua y recursos educativos pertinentes. Tal como enfatiza Lugo, necesitamos “modelos más relevantes, más inclusivos y más flexibles” (2017).

Considero que el compromiso con las metas del ODS 4 no se juega solo en la agenda internacional ni en los grandes programas nacionales, sino también en nuestras aulas, donde cada decisión didáctica y cada planificación puede (y debe) contribuir a sostener y enriquecer trayectorias. Allí donde el árbol no tape el bosque, sino que forme parte viva del ecosistema educativo.



Lugo, M. T. (2017). Políticas TIC en América Latina. Conferencia inaugural de la Cátedra Mapfre-Guanarteme, Universidad de La Laguna. 

UNESCO (2015). Declaración de Incheon y Marco de Acción ODS 4 – Educación 2030. 
"""  # Puedes continuar el texto completo si deseas

salida_larga = output_dir / "narracion.mp3"

response = client.audio.speech.create(
    model='gpt-4o-mini-tts',
    voice='coral',
    input=texto_largo
)
response.stream_to_file(salida_larga)
print(f"[✓] Audio largo guardado en: {salida_larga}")

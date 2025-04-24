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
"""texto_breve = "Suscríbete al canal para apoyar la creación de contenido técnico."
salida_breve = output_dir / "breve.mp3"

# Generar audio
response = client.audio.speech.create(
    model='gpt-4o-mini-tts',
    voice='coral',
    input=texto_breve
)
response.stream_to_file(salida_breve)
print(f"[✓] Audio breve guardado en: {salida_breve}")
"""
# Texto largo ()
texto_largo = """
Ven a estudiar Informática! Tenemos los mejores docentes y servicios: cafetería, biblioteca, sala de informática, salones con televisores y aires acondicionados. 
Y no olvidarnos que podes contar con residencia estudiantil con los mejores cocineros de todo el Uruguay. 
También tenemos a disposición transporte, coloquialmente llamado "el amarillo".
No dejes pasar esta oportunidad, inscribete ya en cerpsw.cfe.edu.uy
"""  # Puedes continuar el texto completo si deseas

salida_larga = output_dir / "narracion_onyx.mp3"

response = client.audio.speech.create(
    model='gpt-4o-mini-tts',
    voice='onyx',
    input=texto_largo
)
response.stream_to_file(salida_larga)
print(f"[✓] Audio largo guardado en: {salida_larga}")
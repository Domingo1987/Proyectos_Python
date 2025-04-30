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

# Texto largo (fragmento de El Principito)
texto_largo = """

La implementación de tecnologías emergentes, particularmente la Inteligencia Artificial (IA), presenta tanto desafíos significativos como oportunidades concretas en el contexto específico del Centro Regional de Profesores (CeRP) del Suroeste. El problema previamente identificado, relacionado con la limitada integración efectiva de herramientas tecnológicas por parte del cuerpo docente, podría abordarse eficazmente mediante la adopción de políticas institucionales claras y una formación docente enfocada específicamente en la IA generativa (IAGen). La UNESCO (2024, p. 18) resalta la importancia de regular la IA generativa desde un enfoque centrado en el ser humano, asegurando así su uso ético, seguro y equitativo, aspecto esencial para una implementación pedagógica adecuada en nuestra institución.
Un desafío particular en el CeRP del Suroeste es la persistente brecha digital, susceptible de ampliarse con la adopción acelerada de tecnologías avanzadas. Según la UNESCO, la IAGen podría agravar la pobreza digital debido a la considerable cantidad de datos y recursos computacionales que demanda, limitando su acceso principalmente a instituciones con mayores recursos económicos y técnicos (UNESCO, 2024, p. 14). Esta situación resulta crítica considerando que el CeRP atiende una población estudiantil heterogénea, lo cual podría profundizar inequidades tecnológicas preexistentes.
No obstante, la incorporación de la IA también brinda oportunidades significativas, especialmente en la personalización y la optimización de los procesos pedagógicos. De acuerdo con Jara y Ochoa (2020, p. 8), existe un consenso sobre el valor de una educación personalizada, capaz de adaptarse eficazmente a las características y dificultades individuales de cada estudiante. En nuestro contexto, esta capacidad permite responder de manera más eficiente a las necesidades particulares en la formación docente, favoreciendo la implementación de estrategias educativas diferenciadas y eficaces.
En este sentido, Holmes (2019, p. 160) advierte que, si bien la IA no reemplazará a los docentes, transformará progresivamente su rol, permitiendo un uso más eficiente de su tiempo y una mejor valorización y ampliación de su experiencia profesional. Esta visión se vincula directamente con la situación actual en nuestra institución, particularmente en la Unidad Curricular de Inteligencia Artificial del profesorado de Informática, donde los estudiantes han socializado sus aprendizajes a través de publicaciones y videos en la plataforma institucional (https://1001problemas.com/ia/). Estos proyectos reflejan no solo el dominio técnico de las herramientas, sino también una reflexión crítica sobre su aplicabilidad pedagógica y los desafíos éticos que su uso conlleva.
Asimismo, la realización del taller interdisciplinario de fin de año, que reunió a más de 50 participantes entre estudiantes y docentes de múltiples áreas, constituye un ejemplo efectivo de socialización de conocimientos y experiencias relacionadas con la IA. Esta actividad responde precisamente a la necesidad señalada por la UNESCO (2024, p. 26), que enfatiza la importancia de formar competencias específicas en IA para un uso ético y significativo por parte de docentes e investigadores.
El aspecto final que mencionaré es que la validación ética y pedagógica de las herramientas de IAGen representa otro desafío relevante para la institución. Según la UNESCO (2024, p. 25), las instituciones educativas deben monitorear y validar cuidadosamente estas tecnologías para asegurar aplicaciones adecuadas y beneficiosas en términos educativos. Esto implica un desafío organizacional importante para el CeRP, exigiendo el desarrollo de políticas internas claras y procesos transparentes de evaluación.
Abordar estos desafíos y aprovechar las oportunidades de la IA exige una acción institucional coordinada, orientada hacia la equidad tecnológica y la formación específica del cuerpo docente, vinculándose estrechamente con los problemas identificados en etapas anteriores del portafolio. Estas experiencias no sólo anticipan cambios en la práctica docente, sino que ofrecen insumos valiosos para el diseño de propuestas pedagógicas más ajustadas a los desafíos contemporáneos que enfrentamos como formadores docentes.

Bibliografía:
Holmes, W., Bialik, M. & Fadel, C. (2019). Artificial Intelligence in Education: Promises and implications for teaching and learning. Boston, MA, Center for Curriculum Redesign
Jara, I., & Ochoa, M. (2020). Usos y efectos de la inteligencia artificial en educación. Fundación Ceibal.
UNESCO. (2024). Guía para el uso de IA generativa en educación e investigación. Organización de las Naciones Unidas para la Educación, la Ciencia y la Cultura.

"""  # Puedes continuar el texto completo si deseas

# Instrucciones para la voz: Patient Teacher
instrucciones = """
Voice Affect: Calm, composed, and reassuring; project quiet authority and confidence.
Tone: Sincere, empathetic, and gently authoritative—express genuine apology while conveying competence.
Pacing: Steady and moderate; unhurried enough to communicate care, yet efficient enough to demonstrate professionalism.
Emotion: Genuine empathy and understanding; speak with warmth, especially during apologies ("I'm very sorry for any disruption...").
Pronunciation: Clear and precise, emphasizing key reassurances ("smoothly," "quickly," "promptly") to reinforce confidence.
Pauses: Brief pauses after offering assistance or requesting details, highlighting willingness to listen and support.
"""

salida_larga = output_dir / "desafios.mp3"

with client.audio.speech.with_streaming_response.create(
    model='gpt-4o-mini-tts',
    voice='sage',
    input=texto_largo,
    instructions=instrucciones,
    response_format="mp3"  # ✅ especificás el formato aquí
) as response:
    with open(salida_larga, "wb") as f:
        for chunk in response.iter_bytes():
            f.write(chunk)


print(f"[✓] Audio largo guardado en: {salida_larga}")

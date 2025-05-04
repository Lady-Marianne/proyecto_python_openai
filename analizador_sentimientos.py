from openai import OpenAI
from dotenv import load_dotenv
import os
import openai
import textwrap
import re

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY_2"))
# Error de autenticación a propósito:
# cliente = OpenAI(api_key="mariana_key")

modelo = "gpt-4o-mini"
# Error de modelo a propósito:
# modelo = "gpt-4o-mariana"

def carga(nombre_archivo):
  try:
    with open(nombre_archivo, "r") as archivo:
      datos = archivo.read()
      return datos
  except IOError as e:
    print(f"Error es: {e}")

def guardar(nombre_archivo,contenido):
  try:
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
      archivo.write(contenido)
  except IOError as e:
      print(f"Error al guardar el archivo {e}")

def analizador_sentimientos(producto):

  prompt_sistema = """
  Eres un analizador de sentimientos de reseñas de productos.
  Escribe un párrafo de hasta 50 palabras resumiendo las reseñas y luego asigna cuál es el
  sentimiento general para el producto. Identifica también 3 puntos fuertes y 3 puntos débiles
  identificados a partir de las reseñas.
  # Formato de Salida:
    - Nombre del Producto:
    - Resumen de las Reseñas:
    - Sentimiento General: [utiliza aquí solo Positivo, Negativo o Neutro].
    - Puntos fuertes: lista con tres puntos fuertes.
    - Puntos débiles: lista con tres puntos débiles.
  """

  prompt_usuario = carga(f"datos/{producto}.txt")
  print(f"Inició el analisis de sentimiento del producto {producto}.")

  lista_mensajes = [
    {
      "role": "system",
      "content": prompt_sistema
    },
    {
      "role": "user",
      "content": prompt_usuario
    }
  ]

  try:
    respuesta = cliente.chat.completions.create(
      messages = lista_mensajes,
      model = modelo
    )

    texto_respuesta = respuesta.choices[0].message.content

    # --- FORMATEAR SÓLO EL RESUMEN DE LAS RESEÑAS ---
    patron = r"(?<=Resumen de las Reseñas:\s)(.*?)(?=\n\s*- Sentimiento General:)"
    coincidencia = re.search(patron, texto_respuesta, re.DOTALL)

    if coincidencia:
        resumen_original = coincidencia.group(0).strip()
        resumen_formateado = textwrap.fill(resumen_original, width=80)
        texto_respuesta = texto_respuesta.replace(resumen_original, resumen_formateado)

    guardar(f"datos/lote_analisis_{producto}.txt", texto_respuesta)

  except openai.AuthenticationError as e:
    print(f"Error de autenticación: {e}")
  except openai.APIError as e:
    print(f"Error de conexión a la API es: {e}")

lista_productos = ["evaluaciones_camisetas_algodon","evaluaciones_jeans_reciclados","evaluaciones_maquillaje"]

for producto in lista_productos:
  analizador_sentimientos(producto)
  print(f"Finalizó el análisis de sentimiento del producto {producto}.")
  print("--------------------------------------------------")
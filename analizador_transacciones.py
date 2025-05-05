from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY_2"))
modelo = "gpt-4o-mini"
temperatura = 0

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

def generar_informe(transaccion):
  print("2. Generando el informe de cada transacción catalogada como posible fraude:\n")

  prompt_sistema = f"""
  Para la siguiente transacción, proporciona un parecer, solamente si su estado es de "Posible Fraude".
  Indica en el informe una justificación por la cual fue identificada como un fraude.
  Transacción: {transaccion}
  # Formato Salida:
  "ID Transacción": "id",
  "Tipo de Transacción": "Crédito o Débito",
  "Establecimiento": "nombre del establecimiento",
  "Horario": "aaaa-mm-dd hh:mm:ss",
  "Producto": "nombre producto",
  "Ciudad - Estado": "Ciudad - Departamento (País)",
  "Valor (USD)": valor número entero,
  "Estado": "Aprobado o Posible Fraude",
  "Informe": "informe con las posibles indicaciones"
  """

  lista_mensajes = [
    {
      "role": "system",
      "content": prompt_sistema
    }
  ]

  respuesta = cliente.chat.completions.create(
    messages = lista_mensajes,
    model = modelo,
    temperature = temperatura
  )

  contenido = respuesta.choices[0].message.content

  return contenido


def analizador_transacciones(lista_transacciones):
  print("1. Realizando el análisis de transacciones:\n")

  prompt_sistema = """
  Analiza las transacciones financieras a continuación e identifica si cada una de ellas es un 
  "Posible Fraude" o debe ser "Aprobada".
  Agrega un atributo "Estado" con uno de los valores: "Posible Fraude" o "Aprobado".
  Cada nueva transacción debe ser insertada dentro de la lista del JSON.
  # Posibles indicaciones de fraude:
  - Transacciones con valores muy discrepantes.
  - Transacciones que ocurren en lugares muy distantes entre sí.
  Adopta el formato de respuesta a continuación para componer tu respuesta.
  # Formato Salida:
  {
    "transacciones": [
      {
        "ID Transacción": "id",
        "Tipo de Transacción": "Crédito o Débito",
        "Establecimiento": "nombre del establecimiento",
        "Horario": "aaaa-mm-dd hh:mm:ss",
        "Producto": "nombre producto",
        "Ciudad - Estado": "Ciudad - Departamento (País)",
        "Valor (USD)": valor numero entero,
        "Estado": "Posible Fraude o Aprobado"
      },
    ]
  }
  """

  prompt_usuario = f"""
  Considera el CSV a continuación, donde cada línea es una transacción diferente: {lista_transacciones}. 
  Tu respuesta debe adoptar el # Formato Salida (solo un json sin otros comentarios)."
  """

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

  respuesta = cliente.chat.completions.create(
    messages=lista_mensajes,
    model= modelo,
    temperature = temperatura
  )

  contenido = respuesta.choices[0].message.content
  print("\n")
  print("contenido:")
  print("\n")
  print(contenido)

  contenido = contenido.strip("```json")
  json_resultado = json.loads(contenido)
  print("\n")
  print(json_resultado)

  return json_resultado

def generar_recomendacion(informe):
  print("3. Generando recomendaciones:\n")

  prompt_sistema = f"""
  Para la siguiente transacción, proporciona una recomendación apropiada basada en el estado y los 
  detalles de la transacción: {informe}.
  Las recomendaciones pueden ser "Notificar Cliente", "Activar sector Anti-Fraude" o "Realizar 
  Verificación Manual".
  Deben ser escritas en un formato técnico.
  Incluye también una clasificación del tipo de fraude, si es aplicable.
  """

  lista_mensajes = [
    {
      "role": "system",
      "content": prompt_sistema
    }
  ]

  respuesta = cliente.chat.completions.create(
    messages = lista_mensajes,
    model = modelo,
    temperature= temperatura
  )

  contenido = respuesta.choices[0].message.content

  return contenido


lista_transacciones = carga("datos/transacciones.csv")
transacciones_analizadas = analizador_transacciones(lista_transacciones)
  
for transaccion in transacciones_analizadas["transacciones"]:
  if transaccion["Estado"] == "Posible Fraude": 
    informe = generar_informe(transaccion)
    print(informe)
    recomendacion = generar_recomendacion(informe)
    id_transaccion = transaccion["ID Transacción"]
    nombre_producto = transaccion["Producto"]
    estado_transacción = transaccion["Estado"]

guardar(f"datos/recomendacion-{id_transaccion}-{nombre_producto}-{estado_transacción}.txt",recomendacion)









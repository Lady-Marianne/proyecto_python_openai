# seleccion_modelo.py

from openai import OpenAI  # Importa la clase OpenAI desde la librería openai
from dotenv import load_dotenv  # Permite cargar las variables de entorno desde un archivo .env
import os  # Proporciona funciones para interactuar con el sistema operativo
import tiktoken  # Librería para contar tokens según el modelo de OpenAI

load_dotenv()  # Carga las variables del archivo .env al entorno de ejecución

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY_2"))  # Crea un cliente OpenAI usando la API Key del entorno

modelo = "gpt-4o"  # Se define inicialmente que se usará el modelo GPT-4o

# Función que carga un archivo de texto y devuelve su contenido como string
def carga(nombre_archivo):
  try:
    with open(nombre_archivo, "r") as archivo:
      datos = archivo.read()
      return datos
  except IOError as e:
    print(f"Error es: {e}")  # Si falla, imprime el error

# Mensaje del sistema para guiar al modelo (rol system)
prompt_sistema = """
Identifique el perfil de compra de cada cliente.
El formato de salida debe ser:
cliente - describa el perfil del cliente en 3 palabras.
"""

# Carga los datos del usuario desde un archivo CSV
prompt_usuario = carga("datos\lista-compra-300-clientes.csv")

# Codifica todo el prompt (sistema + usuario) en tokens para saber cuánto ocupa
codificador = tiktoken.encoding_for_model(modelo)
lista_tokens = codificador.encode(prompt_sistema + prompt_usuario)

print("modelo:", modelo)
print("lista tokens:", lista_tokens)
numero_tokens_entrada =  len(lista_tokens)  # Cuenta los tokens totales del prompt
print(f"Número de tokens: {numero_tokens_entrada}")

tokens_salida = 2048  # Tokens que se le permite generar de salida
limite_TPM_modelo = 10_000  # Límite máximo de tokens por minuto

# Si la suma de tokens de entrada y salida supera el límite, cambiamos de modelo
if numero_tokens_entrada + tokens_salida >= limite_TPM_modelo:
  modelo = "gpt-4o-mini"  # Se pasa a un modelo más liviano

print("modelo:", modelo)  # Se imprime cuál modelo se usará finalmente

# Se realiza la solicitud a la API de OpenAI
respuesta = cliente.chat.completions.create(
  messages = [
    {
      "role": "system",
      "content": prompt_sistema
    },
    {
      "role": "user",
      "content": prompt_usuario
    }
  ],
  model = modelo,
  max_tokens = tokens_salida           
) 

# Imprime el contenido de la respuesta generada
print(respuesta.choices[0].message.content)


# contador_tokens.py

import tiktoken  # Importa la librería para codificación de tokens

modelo = "gpt-4o"  # Se usa primero el modelo gpt-4o
codificador = tiktoken.encoding_for_model(modelo)  # Se obtiene el codificador para ese modelo

# Texto largo que se va a codificar para estimar cuántos tokens ocupa
lista_tokens = codificador.encode(
"""
Eres un categorizador de productos.
Debes asumir las categorías presentes en la lista a continuación.

# Lista de Categorías Válidas:
1. Cat. 1
2. Cat. 2
3. Cat. 3

# Formato de Salida:
Producto: Nombre del Producto
Categoría: presenta la categoría del producto

# Ejemplo de Salida:
Producto: Cepillo de dientes con carga solar
Categoría: Electrónicos Verdes
"""
)

print("modelo:", modelo)
print("lista tokens:", lista_tokens)
print("Número de tokens:", len(lista_tokens))  # Se imprime cuántos tokens ocupa el texto
print(f"Costo para el modelo: {modelo} es de {(2.5*len(lista_tokens)/1_000_000)}")  # Estima el costo

print("\n")

modelo = "gpt-4o-mini"  # Cambia al modelo más económico
print("modelo:", modelo)
print("lista tokens:", lista_tokens)
print("Número de tokens:", len(lista_tokens))
print(f"Costo para el modelo: {modelo} es de {(0.15*len(lista_tokens)/1_000_000)}")  # Estima el costo

print("\n")

# Compara cuánto más caro es el modelo gpt-4o respecto al mini
print(f"El costo del gpt-4o es mayor en {2.5/0.15} que el gpt-4o-mini")

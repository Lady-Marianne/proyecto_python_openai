from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY_2"))

modelo = "gpt-4o"

def carga(nombre_archivo):
  try:
    with open(nombre_archivo, "r") as archivo:
      datos = archivo.read()
      return datos
  except IOError as e:
    print(f"Error es: {e}")

prompt_sistema = """
Identifique el perfil de compra de cada cliente.
El formato de salida debe ser:
cliente - describa el perfil del cliente en 3 palabras.
"""

prompt_usuario = carga("datos\lista-compra-300-clientes.csv")

codificador = tiktoken.encoding_for_model(modelo)
lista_tokens = codificador.encode(prompt_sistema + prompt_usuario)

print("modelo:", modelo)
print("lista tokens:", lista_tokens)
numero_tokens_entrada =  len(lista_tokens)
print(f"Número de tokens: {numero_tokens_entrada}")

tokens_salida = 2048
limite_TPM_modelo = 10_000

if numero_tokens_entrada + tokens_salida >= limite_TPM_modelo:
  modelo = "gpt-4o-mini"

print("modelo:", modelo)

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

print(respuesta.choices[0].message.content)
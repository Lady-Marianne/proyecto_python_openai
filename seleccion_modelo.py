from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_2"))
modelo = "gpt-4o"

codificador = tiktoken.encoding_for_model(modelo)

def carrega(nombre_del_archivo):
    try:
        with open(nombre_del_archivo, "r") as archivo:
            datos = archivo.read()
            return datos
    except IOError as e:
        print(f"Error: {e}")

prompt_sistema = """
Identifica el perfil de compra para cada cliente a continuación.

El formato de salida debe ser:

cliente - describe el perfil del cliente en 3 palabras
"""

prompt_usuario = carrega("datos\lista_de_compras_300_clientes.csv")

lista_de_tokens = codificador.encode(prompt_sistema + prompt_usuario)
numero_de_tokens = len(lista_de_tokens)
print(f"Número de tokens en la entrada: {numero_de_tokens}")
tamaño_esperado_salida = 2048

if numero_de_tokens >= 4096 - tamaño_esperado_salida:
    modelo = "gpt-4o-mini"

print(f"Modelo elegido: {modelo}")

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

respuesta = client.chat.completions.create(
    messages = lista_mensajes,
    model=modelo
)

print(respuesta.choices[0].message.content)
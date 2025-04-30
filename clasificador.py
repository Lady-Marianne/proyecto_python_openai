from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY_2"))
modelo = "gpt-4o-mini"

def categoriza_producto(nombre_producto, lista_categorias_posibles):
    prompt_sistema = f"""
        Eres un categorizador de productos.
        Debes asumir las categorías presentes en la lista a continuación:

        # Lista de Categorías Válidas:
        {lista_categorias_posibles.split(",")}

        # Formato de Salida:
        Producto: Nombre del Producto.
        Categoría: Presenta la categoría del producto.

        # Ejemplo de Salida:
        Producto: Cepillo eléctrico con recarga solar.
        Categoría: Electrónicos Verdes.
    """

    respuesta = cliente.chat.completions.create(
        messages=[
            {
                "role":"system",
                "content" : prompt_sistema
            },
            {
                "role" : "user",
                "content" : nombre_producto
            }

        ],
        model=modelo,
        temperature = 1,
        max_tokens=200
    )

    return respuesta.choices[0].message.content

categorias_validas = input("Informa las categorías válidas, separando por comas: ")

while True:
    nombre_producto = input("Escribe el nombre del producto: ")
    texto_respuesta = categoriza_producto(nombre_producto, categorias_validas)
    print(texto_respuesta)
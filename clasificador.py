from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize OpenAI API client:
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY_2"))
modelo  = "gpt-4o-mini"
prompt_sistema = f"""
        Eres un categorizador de productos.
        Debes asumir las categorías presentes en la lista a continuación.

        # Lista de Categorías Válidas
        {lista_categorias_posibles.split(",")}

        # Formato de Salida
        Producto: Nombre del Producto
        Categoría: presenta la categoría del producto

        # Ejemplo de Salida
        Producto: Cepillo eléctrico con recarga solar
        Categoría: Electrónicos Verdes

    """

respuesta = cliente.chat.completions.create(
    messages=[
    {
        "role": "system",
        "content": """
        Clasifica el producto a continuación en una de las siguientes categorías:
        1. Higiene personal
        2. Moda
        3. Casa
        Además, crea una descripción de la categoría.
        """
    },
    {
        "role": "user",
        "content": "Cepillo de dientes de bambú"
    }
    ],
    model=modelo,
    temperature=1,
    max_tokens=200
    )

print(respuesta.choices[0].message.content)
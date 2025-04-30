from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize OpenAI API client:
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY_2"))

respuesta = cliente.chat.completions.create(
    messages=[
    {
        "role": "system",
        "content": """
        Eres un asistente de un e-commerce de productos sustentables.
        Cuando te pidan productos, devuelve sólo el nombre del producto sin considerar la descripción.
        """
    },
    {
        "role": "user",
        "content": "Lista 3 productos sustentables."
    }
    ],
    model="gpt-4o-mini"
)

print(respuesta.choices[0].message.content)
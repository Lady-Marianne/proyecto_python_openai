import tiktoken

modelo = "gpt-4o-mini"
codificador = tiktoken.encoding_for_model(modelo)
lista_tokens = codificador.encode("Eres un categorizador de productos.")

print("Lista de Tokens: ", lista_tokens)
print("¿Cuántos tokens tenemos?: ", len(lista_tokens))
print(f"Costo para el modelo {modelo} es de ${(len(lista_tokens)/1000000) * 0.15}")

modelo = "gpt-4o"
codificador = tiktoken.encoding_for_model(modelo)
lista_tokens = codificador.encode("Eres un categorizador de productos.")

print("Lista de Tokens: ", lista_tokens)
print("¿Cuántos tokens tenemos?: ", len(lista_tokens))
print(f"Costo para el modelo {modelo} es de ${(len(lista_tokens)/1000000) * 2.50}")

print(f"El costo del GPT-4o es de {2.5/0.15} mayor que el del GPT-4o-mini")
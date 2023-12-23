# ----- Criar fake api para nosso projeto. ----- #
import os
import random

import pandas as pd
from faker import Faker
from fastapi import FastAPI

# Criar serviço de API.
app = FastAPI()

# Criar objeto Faker para gerar nomes aleatórios.
fake = Faker()

# Importar arquivo de produtos.
file_name = f"{os.getcwd()}/backend/fake-api/products.csv"

# Armazenar lista em DataFrame.
df = pd.read_csv(file_name)

# Criar índice para retornar e coletar linha de maneira randomizada.
df["indice"] = range(1, len(df) + 1)
df.set_index("indice", inplace=True)

# Criar variável com número de loja padrão online.
loja_padrao_online = 11


# Criar as rotas.
@app.get("/gerar_compra")
async def gerar_compra():
    index = random.randint(1, len(df) - 1)
    tuple = df.iloc[index]
    return {
        "client": fake.name(),
        "creditcard": fake.credit_card_provider(),
        "product": tuple["Product Name"],
        "ean": int(tuple["EAN"]),
        "price": round(float(tuple["Price"]) * 1.2, 2),
        "clientPosition": fake.location_on_land(),
        "store": loja_padrao_online,
        "dateTime": fake.iso8601(),
    }


@app.get("/gerar_compras/{numero_registro}")
async def gerar_compras(numero_registro: int):  # Retorna função assíncrona
    if numero_registro < 1:  # Validar número de compras
        return {"error": "O número deve ser maior que 1"}

    respostas = []

    for _ in range(numero_registro):
        index = random.randint(1, len(df) - 1)
        tuple = df.iloc[index]
        compra = {
            "client": fake.name(),
            "creditcard": fake.credit_card_provider(),
            "product_name": tuple["Product Name"],
            "ean": int(tuple["EAN"]),
            "price": round(float(tuple["Price"]) * 1.2, 2),
            "clientPosition": fake.location_on_land(),
            "store": loja_padrao_online,
            "dateTime": fake.iso8601(),
        }

        respostas.append(compra)

    return respostas

from datetime import date
from enum import Enum

from pydantic import BaseModel, EmailStr, PositiveFloat, validator


class CategoriaEnum(str, Enum):
    categoria_1 = "Categoria 1"
    categoria_2 = "Categoria 2"
    categoria_3 = "Categoria 3"
    categoria_4 = "Categoria 4"
    categoria_5 = "Categoria 5"
    categoria_6 = "Categoria 6"
    categoria_7 = "Categoria 7"
    categoria_8 = "Categoria 8"
    categoria_9 = "Categoria 9"


class Catalogo(BaseModel):
    EAN: int
    Produto: str
    Categoria: CategoriaEnum
    Descricao: str
    Preco: PositiveFloat
    Fornecedor: EmailStr
    Data: date

    @validator("Preco")
    def validador_preco(cls, v):
        """
        Valida o preço do produto.
        """
        if v <= 0:
            raise ValueError("O preço deve ser maior que zero.")
        return v

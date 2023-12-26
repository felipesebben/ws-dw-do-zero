# Definir schema genérico a ser seguido.
from typing import Dict, Union

GenericSchema = Dict[str, Union[str, float, int]]


CompraSchema: GenericSchema = {
    "ean": int,
    "price": float,
    "store": int,
    "dateTime": str,
}

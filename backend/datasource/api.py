from typing import List

import requests
from contracts.schema import CompraSchema, GenericSchema


class APICollector:
    def __init__(self, schema):
        self._schema = schema
        self._aws = None
        self._buffer = None
        return

    def start(self, param):
        response = self.getData(param)
        response = self.extractData(response)
        return response

    def getData(self, param):
        response = None
        if param > 1:
            response = requests.get(
                f"http://127.0.0.1:8000/gerar_compras/{param}"
            ).json()
        else:
            response = requests.get("http://127.0.0.1:8000/gerar_compra").json()
            if isinstance(response, dict):
                response = [response]
        return response

    def extractData(self, response):
        result: List[GenericSchema] = []
        for item in response:
            index = {}
            for key, value in self._schema.items():
                if type(item.get(key)) == value:
                    index[key] = item[key]
                else:
                    index[key] = None
            result.append(index)
        return result

    def transformDf(self):
        return

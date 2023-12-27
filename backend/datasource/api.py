import datetime as dt
from io import BytesIO
from typing import List

import pandas as pd
import pyarrow.parquet as pq
import requests
from contracts.schema import CompraSchema, GenericSchema


class APICollector:
    def __init__(self, schema, aws):
        self._schema = schema
        self._aws = aws
        self._buffer = None
        return

    def start(self, param):
        """
        Inicia a coleta de dados.
        """
        response = self.getData(param)
        response = self.extractData(response)
        response = self.transformDf(response)
        response = self.convertToParquet(response)

        if self._buffer is not None:
            file_name = self.fileName()
            print(file_name)
            self._aws.upload_file(response, file_name)
            return True
        return False

    def getData(self, param):
        """
        Coleta os dados da API.
        """
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
        """
        Extrai os dados do resultado.
        """
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

    def transformDf(self, response):
        """
        Transforma o resultado em um DataFrame.
        """
        result = pd.DataFrame(response)
        return result

    def convertToParquet(self, response):
        """
        Converte o DataFrame em um arquivo parquet.
        """
        self._buffer = BytesIO()
        try:
            response.to_parquet(self._buffer)
            return self._buffer
        except Exception as e:
            print(f"Erro ao converter o DataFrame para parquet: {e}")
            self._buffer = None

    def fileName(self):
        """
        Formata nome do arquivo conforme fonte e data da coleta.
        """
        data_atual = dt.datetime.now().isoformat()
        match = data_atual.split(".")
        return f"api/api-response-compra{match[0]}.parquet"

import openpyxl
import pandas as pd
import streamlit as st
from pydantic import ValidationError


class CSVCollector:
    def __init__(self, schema, aws, cell_range):
        self._schema = schema
        self._aws = aws
        self._buffer = None
        self.cell_range = cell_range
        return

    def start(self):
        """
        Inicia a coleta de dados.
        """
        getData = self.getData()
        extractData = None
        if getData is not None:
            extractData = self.extractData(getData)
        if extractData is not None:
            validateData = self.validateData(extractData)
            return validateData

    def getData(self):
        """
        Coleta dados inseridos pelo arquivo Excel fornecido pelo usuário no frontend.
        """
        dados_excel = st.file_uploader("Insira o arquivo Excel", type="xlsx")
        return dados_excel

    def extractData(self, dados_excel):
        """
        Extrai os dados do resultado.
        """
        workbook = openpyxl.load_workbook(dados_excel)
        sheet = workbook.active
        cell_range = sheet[self.cell_range]
        # Obter o índice 0, que é o cabeçalho.
        headers = [cell.value for cell in cell_range[0]]

        data = []
        for row in cell_range[1:]:
            data.append([cell.value for cell in row])
        dataframe = pd.DataFrame(data, columns=headers)
        return dataframe

    def validateData(self, dataframe):
        error = []
        valid_rows = []

        for index, row in dataframe.iterrows():
            try:
                # Criar instancia do modelo Pydantic para cada linha.
                valid_row = self._schema(**row.to_dict())
                valid_rows.append(valid_row)
            except ValidationError as e:
                # Se houver erro, adicione a mensagem de erro à lista de erros.
                error.append(f"Erro na linha {index + 1} :{str(e)}")
        if error:
            st.error[Exception("\n".join(error))]
            return None  # Retornar None se houver erros

        st.success("Tudo certo!")
        return dataframe

    def loadData(self):
        pass

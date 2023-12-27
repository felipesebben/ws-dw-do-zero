import openpyxl
import pandas as pd
import streamlit as st


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
        if getData is not None:
            extractData = self.extractData(getData)
            return extractData
        else:
            return "Nenhum arquivo foi inserido."

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
        cell_range = sheet[cell_range]
        # Obter o íncide 0, que é o cabeçalho.
        headers = [cell.value for cell in cell_range[0]]

        data = []
        for row in cell_range[1:]:
            data.append([cell.value for cell in row])
        dataframe = pd.DataFrame(data, columns=headers)
        return dataframe

    def validateData(self):
        pass

    def loadData(self):
        pass

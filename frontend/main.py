import streamlit as st
from aws.client import S3Client
from contracts.catalogo import Catalogo
from datasource.csv import CSVCollector

# from aws.client import S3Client
# from datasource.csv import CSVCollector


st.title("Esta é uma página de portal de dados")

# st.file_uploader("Upload de arquivo", type=("png", "jpg", "csv"))


aws_instancia = S3Client()
catalogo_de_produto = CSVCollector(Catalogo, aws_instancia, "C11:I209")
catalogo_de_produto.start()

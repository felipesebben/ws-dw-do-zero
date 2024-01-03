import os
import sys

import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

load_dotenv()

# Presme-se que tu tenhas uma variável de ambiente chamada "MINHA_VARIAVEL"
# É possível acessar o valor dela com a função os.environ.get("MINHA_VARIAVEL")


class S3Client:
    """
    Validar se as variáveis de ambiente necessárias estão definidas.
    Variáveis de ambiente necessárias:
    - `AWS_ACCESS_KEY_ID`
    - `AWS_SECRET_ACCESS_KEY`
    - `AWS_REGION`
    - `S3_BUCKET_NAME`
    - `DELTA_LAKE_S3_PATH`
    \nEm seguida, criar um cliente do S3. O cliente do S3 é responsável por fazer o upload e download de arquivos.
    """

    def __init__(self):
        self._envs = {
            "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
            "region_name": os.environ.get(
                "AWS_REGION", "us-east-1"
            ),  # Usando um valor padrão se a variável não for definida
            "s3_bucket": os.environ.get("S3_BUCKET_NAME"),
            "datalake": os.environ.get("DELTA_LAKE_S3_PATH"),
        }

        for var in self._envs:
            if self._envs[var] is None:
                print(f"A variável de ambiente {var} não foi definida.")
                sys.exit(1)  # Encerra o programa com código de erro 1

        # Criar cliente do S3
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self._envs["aws_access_key_id"],
            aws_secret_access_key=self._envs["aws_secret_access_key"],
            region_name=self._envs["region_name"],
        )

    def upload_file(self, data, s3_key):
        """
        Sobe um arquivo para o S3.
        """
        try:
            self.s3.put_object(
                Body=data.getvalue(), Bucket=self._envs["s3_bucket"], Key=s3_key
            )
        except NoCredentialsError:
            print(
                "Credenciais não encontradas. Certifique-se de que as credenciais da AWS estão configuradas."
            )

    def download_file(self, s3_key):
        """
        Baixa um arquivo do S3.
        """
        try:
            file = self.s3.get_object(Bucket=self._envs["s3_bucket"], Key=s3_key)
            print(f"Download bem sucedido: {s3_key}")
            return file
        except NoCredentialsError:
            print(
                "Credenciais não encontradas. Certifique-se de que as credenciais da AWS estão configuradas."
            )
        except FileNotFoundError:
            print(
                f"Arquivo {s3_key} não encontrado no bucket {self._envs['s3_bucket']}."
            )
        except Exception as e:
            print(f"Ocorreu um erro durante o download do arquivo: {e}")

    def list_object(self, prefix):
        """
        Retorna uma lista de objetos do S3.
        """
        return self.s3.list_objects(Bucket=self._envs["s3_bucket"], Prefix=prefix)[
            "Contents"
        ]

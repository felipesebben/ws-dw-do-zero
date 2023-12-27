import time

import schedule
from aws.client import S3Client
from contracts.schema import CompraSchema, GenericSchema
from datasource.api import APICollector

schema = CompraSchema
aws = S3Client()


def api_collector(schema, aws, repeat: int):
    """
    Chama a classe APICollector para coletar os dados.
    """
    response = APICollector(schema, aws).start(repeat)
    print("Executei a chamada da API.")
    return


schedule.every(1).minutes.do(api_collector, schema, aws, 5)

while True:
    schedule.run_pending()
    time.sleep(1)

from contracts.schema import CompraSchema, GenericSchema
from datasource.api import APICollector

schema = CompraSchema

minha_classe = APICollector(schema).start(1)


print(minha_classe)

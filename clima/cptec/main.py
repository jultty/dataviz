from Aranha import Aranha
from Plotadora import Plotadora
from Tratadora import Tratadora

"""A data scrapper for INPE climate data"""

__version__ = "0.1.0"
def main(cidades):
  # inicializa os objetos
  aranha = Aranha()
  tratadora = Tratadora()
  plotadora = Plotadora()

  # carrega e limpa os dados
  aranha.obter(cidades)
  tratadora.extrair(cidades)
  tratadora.limpar(cidades)

  # exibe os dados no console
  tratadora.exibir(cidades)

  # exporta os dados para csv
  tratadora.exportar(cidades)

  # carrega os dados na plotadora e plota os gráficos
  plotadora.abrir_csv(cidades)
  plotadora.plotar(lista_cidades=cidades, chuva=False, estilo='dark_background')
  plotadora.plotar(lista_cidades=cidades, chuva=True, estilo='dark_background')

  # exibe os meteogramas
  for cd in cidades:
    cd.exibir_meteograma()

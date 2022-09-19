import re
from datetime import date
from pathlib import Path

from babel.dates import format_date
from matplotlib import pyplot as plt, image as img
from unidecode import unidecode


class Cidade:
    """Armazene nome e UF de cada cidade, dados de clima e caminhos de saída.

    Esta classe é passada dentro de uma lista para as demais, que
    inserem e atualizam dados para cada cidade.
    """

    def __init__(self, nome, uf):
        """
        Inicialize um objeto da classe Cidade.

        Este método limpa os valores para nome e uf ao gravá-los no objeto
        para prevenir erros no caminho dos arquivos de saída.

        :param nome: nome da cidade
        :param uf: sigla da unidade federativa (estado)
        :raises ValueError: se a uf não for composta apenas por letras
        """

        self.data = date.today()
        self.data_str = str(self.data)

        try:
            nome_alpha = re.sub('[^a-zA-Z ]', '',
                                unidecode(nome.replace('-', ' ')))

            self.nome = '-'.join(nome_alpha.strip().split()).lower()

            self.uf = ' '.join(uf.lower().strip().split())

            if not self.uf.isalpha():
                raise ValueError

            self.url_remota = 'http://tempo.cptec.inpe.br/' \
                              + self.uf + '/' + self.nome

            nome_base = self.nome + '-' + self.uf + '_' + self.data_str

            self.saida_html = 'html/inpe_' + nome_base + '.html'
            self.saida_csv = 'csv/inpe_' + nome_base + '.csv'
            self.saida_meteograma = 'png/meteograma_' + nome_base + '.png'
            self.saida_plot = 'png/plot_' + nome_base + '.png'
            self.saida_plot_chuva = 'png/plot-chuva_' + nome_base + '.png'
        except ValueError:
            print(' [cidade.init] A UF contém caracteres inválidos')
        except Exception as e:
            print(str(e))

        self.nome_extenso = ''

        self.semana = []

        self.x = []
        self.y_max = []
        self.y_min = []
        self.chuva = []

    def exibir_meteograma(self):
        """Verifique se o meteograma existe e exiba via interface gráfica."""
        try:
            if Path(self.saida_meteograma).exists():
                plt.title('Meteograma: ' + self.nome_extenso + ', ' +
                          format_date(self.data, "d 'de' MMMM",
                                      locale='pt_BR'))
                im = img.imread(self.saida_meteograma)
                plt.imshow(im)
                plt.xticks([])
                plt.yticks([])
                plt.show()
        except FileNotFoundError:
            print(' [tratadora.exibir_meteograma] Imagem não encontrada: ' +
                  self.saida_meteograma)
        except IOError:
            print(' [tratadora.exibir_meteograma] Erro de entrada e saída')
        except Exception as e:
            print(' [tratadora.exibir_meteograma] ' + str(e))

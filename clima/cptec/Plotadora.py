import csv
from datetime import date, datetime

from babel.dates import format_date
from matplotlib import pyplot as plt


class Plotadora:
    """Leia arquivos CSV, gere gráficos e salve em arquivos de imagem."""

    def __init__(self):
        """
        Método construtor da classe Plotadora. Não requer parâmetros.

        Apenas inicializa a data atual e uma versão em português
        contendo o dia e o nome do mês por extenso.
        """
        self.hoje = date(
            datetime.now().year, datetime.now().month, datetime.now().day
        )
        self.hoje_pt = format_date(self.hoje, "d 'de' MMMM", locale='pt_BR')

    def abrir_csv(self, lista_cidades):
        """
        Leia o arquivo CSV e grave os dados no objeto.

        Deve ser usado após o método exportar da classe Tratadora.

        Os dados lidos são gravados diretamente nas propriedades x, y_min,
        y_max e chuva de cada objeto da lista recebida como parâmetro.

        :param lista_cidades: Lista de objetos da classe Cidade
        """

        for c in lista_cidades:
            try:
                f = open(c.saida_csv, 'r')
            except FileNotFoundError:
                print(' [plotadora.abrir_csv] Arquivo csv não foi encontrado')
            except IOError:
                print(' [plotadora.abrir_csv] Erro de entrada e saída')
            except Exception as e:
                print(' [plotadora.abrir_csv] ' + str(e))
            else:
                with f:
                    plot = csv.reader(f)
                    for li, linha in enumerate(plot):
                        if li == 0:
                            continue
                        c.x.append(linha[0] + '\n' + linha[1].split('/')[0])
                        c.y_max.append(float(linha[2]))
                        c.y_min.append(float(linha[3]))
                        c.chuva.append(float(linha[4]))

    def plotar(self, lista_cidades, chuva, estilo):
        """
        Gere os gráficos, salve os arquivos no sistema local e exiba-os.

        Este método passa pelas cidades passadas como parâmetro, gera
        cada gráfico e exibe-o na tela usando o visualizador do matplotlib.

        Deve ser usado após o método abrir_csv.

        :param lista_cidades: Lista de objetos da classe Cidade
        :param chuva: True para incluir dados de chuva ou False para excluir
        :param estilo: estilo do gráfico. Para estilos disponíveis, ver a
                        documentação da biblioteca matplotlib
        """
        for c in lista_cidades:
            try:
                if len(c.semana) > 1:
                    print(' [plotadora.plotar] Plotando ' + c.nome_extenso +
                          ' com ' + str(len(c.semana)) + ' linhas em ' +
                          c.saida_plot)
                    plt.style.use(estilo)
                    plt.plot(c.x, c.y_max,
                             color='orange',
                             label='temp. máx (°C)',
                             linestyle='-')
                    plt.plot(c.x, c.y_min,
                             color='teal',
                             label='temp. min (°C)',
                             linestyle='-')
                    if chuva:
                        plt.plot(c.x, c.chuva,
                                 color='steelblue',
                                 label='prob. chuva (%)',
                                 linestyle='-')
                    plt.xlabel('')
                    plt.legend()
                    plt.title(
                        'Previsão para ' + self.hoje_pt + ' em ' +
                        c.nome_extenso)
                    if chuva:
                        plt.savefig(c.saida_plot_chuva)
                    else:
                        plt.savefig(c.saida_plot)
                    plt.show()
                else:
                    print(' [plotadora.plotar] Dados insuficientes para ' +
                          c.nome + ' com apenas ' + str(len(c.semana))
                          + ' linhas')
            except AttributeError:
                print(' [plotadora.plotar] AttributeError: '
                      'O arquivo CSV para ' + c.nome + ' foi gerado?')
            except Exception as e:
                print(' [plotadora.plotar] ' + str(e))

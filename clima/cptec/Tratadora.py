import csv
import re


class Tratadora:
    """
    Limpe e exporte os dados climáticos de uma lista de cidades.

    Esta classe trata o contéudo HTML retornado pela classe Aranha e pode
    limpar e exportar os dados para CSV para plotagem pela classe Plotadora.

    :param campos: Cabeçalhos do arquivo CSV conforme os dados disponíveis
    """
    campos = ['Dia', 'Data', 'Máx', 'Min', 'Chuva']

    def extrair(self, lista_cidades):
        """
        Extraia os dados do HTML obtido e salve no objeto cidade.

        Este método utiliza os dados contidos no documento HTML para
        obter o nome completo da cidade e os dados meteorológicos para
        cada dia da semana em forma de tags HTML a partir dos seletores CSS.

        É preciso utilizar este método antes dos demais métodos da classe.

        :param lista_cidades: Lista de objetos da classe Cidade
        """

        # define um dicionário com os seletores css correspondentes a cada dado
        sel = {'previsao': 'previsao text-center',
               'estendida': 'proximos-dias text-centerc w-100',
               'final': 'previsao-estendida text-center w-100'}

        for c in lista_cidades:
            try:
                title = c.soup.title.text
                title = ' '.join(title.split())
                title = title.replace('Previsão de Tempo -', '').strip()
                title = title.replace('- Centro de Previsão de Tempo e '
                                      'Estudos Climáticos - INPE', '').strip()
                c.nome_extenso = title

                c.semana.append(c.soup.find_all('div', sel['previsao'])[0])
                c.semana.append(c.soup.find_all('div', sel['previsao'])[1])

                for e in c.soup.find_all('div', sel['estendida']):
                    c.semana.append(e)

                c.semana.append(c.soup.find_all('div', sel['final'])[4])
            except AttributeError:
                print(' [tratadora.extrair] AttributeError: O arquivo HTML ' +
                      'para ' + c.nome + ' foi baixado?')
            except Exception as e:
                print(' [tratadora.extrair] ' + str(e))

    def exibir(self, lista_cidades):
        """
        Exiba os dados atuais de cada cidade no console.

        Funciona apenas após a utilização do método extrair.

        :param lista_cidades: Lista de objetos da classe Cidade
        """

        print()
        for c in lista_cidades:
            try:
                if not len(c.nome_extenso) == 0:
                    print(' [tratadora.exibir] ' + c.nome_extenso + ':')
                for d in c.semana:
                    print(str(d))
                print(c.meteograma + '\n')
            except AttributeError:
                print(' [tratadora.exibir] AttributeError: O arquivo HTML ' +
                      'para ' + c.nome + ' foi baixado?')
            except Exception as e:
                print(' [tratadora.exibir] ' + str(e))

    def limpar(self, lista_cidades):
        """
        Remova caracteres desnecessários e ordene os dados.

        É preciso utilizar primeiro o método extrair para popular a
        propriedade semana de cada objeto da lista.

        A posição dos dados no HTML difere para os dois primeiros dias,
        (dia atual e seguinte), necessitando reordenar os dados.
        Os números nas listas ordem_inicio e ordem_fim correspondem
        à posição dos campos 'Dia', 'Data', 'Máx', 'Min' e 'Chuva' depois
        que as demais palavras são removidas.

        :param lista_cidades: Lista de objetos da classe Cidade
        """

        for c in lista_cidades:
            # remove palavras desnecessárias, deixando apenas os dados

            filtro = ['Índice UV [0-9]{1,2}', 'Prob. de Chuva', 
                      'Temperatura', '[0-9]{2}:[0-9]{2}', '-Feira', 'Manhã', 
                      'Tarde', 'Noite', '%', '°']
            try:
                for d, dia in enumerate(c.semana):
                    c.semana[d] = ' '.join(c.semana[d].text.split())
                    for f in filtro:
                        c.semana[d] = re.sub(f, '', c.semana[d])
                    c.semana[d] = ' '.join(c.semana[d].split())
            except AttributeError:
                print(' [tratadora.limpar] AttributeError: O arquivo HTML ' +
                      'para ' + c.nome + ' foi baixado?')
            except Exception as e:
                print(' [tratadora.limpar] Erro ao limpar dia' + 
                      d + ': ' +  str(e))

            # inicializa uma lista vazia que conterá um dia em cada posição
            linhas = []

            ordem_inicio = [0, 1, 3, 4, 2]  # dia atual e dia seguinte
            ordem_fim = [0, 1, 3, 2, 4]  # demais dias

            # varre os dados atuais da semana no objeto
            try:
                for d, dia in enumerate(c.semana):
                    dia_split = dia.split()
                    linha = []

                    # para o dia atual e dia seguinte
                    if d < 2:
                        # se há dados para manhã, tarde e noite,
                        # substituir os três valores pela média
                        if len(dia_split) == 7:
                            dia_split[2] = (float(dia_split[2]) + float(
                                dia_split[3]) + float(dia_split[4])) / 3
                            del dia_split[3:5]
                        # se há dados para tarde e noite, substituir pela média
                        elif len(dia_split) == 6:
                            dia_split[2] = (int(dia_split[2]) + int(
                                dia_split[3])) / 2
                            del dia_split[3]

                        # adiciona cada dado na ordem
                        for i in ordem_inicio:
                            linha.append(dia_split[i])

                    # para os demais dias, apenas adiciona na ordem
                    else:
                        for i in ordem_fim:
                            linha.append(dia_split[i])

                    # converte os dados numéricos para o tipo float
                    linha[2] = float(linha[2])
                    linha[3] = float(linha[3])
                    linha[4] = float(linha[4])

                    # adiciona os dados ao atributo semana do objeto
                    linhas.append(linha)
                    c.semana[d] = linha

                    # saída para  debug
                    print(' [tratadora.limpar] linha processada: ' + str(linha))
            except AttributeError:
                print(' [tratadora.limpar] AttributeError: O arquivo HTML ' +
                      'para ' + c.nome + ' foi baixado?')
            except Exception as e:
                print(' [tratadora.limpar] Erro na varredura: ' + str(e) +
                      ' na linha ' + str(linha))

    def exportar(self, lista_cidades):
        """
        Crie um arquivo CSV com os dados limpos.

        Deve ser utilizado após os métodos extrair e limpar

        :param lista_cidades: Lista de objetos da classe Cidade
        """

        for c in lista_cidades:
            try:
                saida_csv = open(c.saida_csv, 'w')
            except IOError:
                print(' [tratadora.exportar] Erro de entrada e saída')
            except Exception as e:
                print(' [tratadora.exportar] ' + str(e))
            else:
                with saida_csv:
                    try:
                        csv_writer = csv.writer(saida_csv)
                        csv_writer.writerow(self.campos)
                        print(' [tratadora.exportar] Pronta para gravar ' +
                              str(len(c.semana)) + ' linhas')
                    except AttributeError:
                        print(' [tratadora.exportar] AttributeError: O ' +
                              'arquivo HTML para ' + c.nome + ' foi baixado?')
                    except Exception as e:
                        print(' [tratadora.exportar] ' + str(e))
                    else:
                        for dia in c.semana:
                            csv_writer.writerow(dia)
                        print(' [tratadora.exportar] Dados exportados')

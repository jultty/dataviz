from pathlib import Path

import requests
from bs4 import BeautifulSoup


class Aranha:
    """
    Busque dados no sistema local e realize requisições pela web.

    Esta classe possui apenas um método público, obter(), que chama
    os demais métodos privados obter_remoto(), __obter_local() e
     __obter_meteograma.

     Os métodos privados retornam um objeto BeautifulSoup, mas ele nunca
     é retornado para fora da classe pelo método público obter() e sim
     salvo na propriedade soup de cada objeto da classe Cidade.
    """

    def obter(self, lista_cidades):
        """
        Verifique se os arquivos locais já existem e obtenha da rede.

        Este método determina se os arquivos locais para a data atual existem
        e busca-os da rede em caso negativo, solicitando antes a confirmação
        para cada requisição externa.

        Após obter os dados na forma de um arquivo HTML, eles são salvos
        em um objeto BeautifulSoup que é então gravado no atributo soup
        de cada objeto Cidade.

        :param lista_cidades: lista com objetos da classe Cidade
        """

        for c in lista_cidades:
            try:
                if not Path(c.saida_html).exists():
                    confirma = input(
                        '[aranha.obter] ' + c.saida_html +
                        ' não encontrado. Deseja baixar? [s/N] ')
                    if confirma == 'S' or confirma == 's':
                        c.soup = self.__obter_remoto(c)
                    else:
                        input('[aranha.obter] Requisição não executada. ' +
                              'Pressione ENTER para continuar: ')
                else:
                    print(' [aranha.obter] ' + c.saida_html + ' encontrado ')
                    c.soup = self.__obter_local(c)
            except AttributeError:
                print(' [aranha.obter] AttributeError: A cidade ' +
                      c.nome + ' foi inicializada corretamente?')
            except Exception as e:
                print(' [aranha.obter] ' + str(e))

            try:
                sel = 'img-fluid rounded mx-auto d-block'
                c.meteograma = c.soup.find('img', class_=sel).get('src')

                if Path(c.saida_meteograma).exists():
                    print(' [aranha.obter_meteograma] ' + c.saida_meteograma +
                          ' encontrado')
                else:
                    confirma = input(
                        '[aranha.obter_meteograma] ' + c.saida_meteograma +
                        ' não encontrado. Deseja baixar? [s/N] ')
                    if confirma == 'S' or confirma == 's':
                        print(' [aranha.obter_meteograma] Baixando ' +
                              c.saida_meteograma)
                        self.__obter_meteograma(c)
                    else:
                        input('[aranha.obter] Requisição não executada. ' +
                              'Pressione ENTER para continuar: ')
            except AttributeError:
                print(' [aranha.obter] AttributeError: A cidade ' +
                      c.nome + ' foi inicializada corretamente?')
            except Exception as e:
                print(' [aranha.obter] ' + str(e))

    def __obter_remoto(self, c):
        """"
        Busque dados através de uma requisição GET para a url remota.

        Este método faz uma requisição HTTP externa.

        :rtype: BeautifulSoup object
        :param c: cidade passada pelo método público obter()
        :return: BeautifulSoup object soup
        """

        try:
            with open(c.saida_html, 'w') as local:
                print(' [aranha.obter_remoto] Obtendo arquivo remoto de: ' +
                      c.url_remota)
                resposta = requests.get(c.url_remota)
                print(' [aranha.obter_remoto] Resposta: ' + str(resposta))
                soup = BeautifulSoup(resposta.content, 'html.parser')
                local.write(soup.prettify())
        except Exception as e:
            print(' [aranha.obter_remoto] ' + str(e))
        return soup

    def __obter_local(self, c):
        """
        Carregue dados já existentes no sistema local.

        :rtype: BeautifulSoup object
        :param c: cidade passada pelo método público obter()
        :return: BeautifulSoup object soup
        """

        try:
            local = open(c.saida_html, 'r')
        except FileNotFoundError:
            print(' [aranha.obter_local] Arquivo HTML para ' +
                  c.nome + ' não encontrado')
        except IOError:
            print(' [aranha.obter_local] Erro de entrada e saída')
        except Exception as e:
            print(' [aranha.obter_local] ' + str(e))
        else:
            with local:
                print(' [aranha.obter_local] Carregando arquivo local ')
                soup = BeautifulSoup(local, 'html.parser')
            return soup

    def __obter_meteograma(self, c):
        """
        Baixe a imagem do meteograma e salve diretamente no sistema local.

        Este método faz uma requisição HTTP externa.

        :param c: cidade passada pelo método público obter()
        """

        resposta = requests.get(c.meteograma)

        if resposta.status_code == 200:
            try:
                with open(c.saida_meteograma, 'wb') as saida:
                    saida.write(resposta.content)
            except IOError:
                print(' [aranha.obter_meteograma] Erro de entrada e saída')
            except Exception as e:
                print(' [aranha.obter_meteograma] ' + str(e))
            else:
                print(' [aranha.obter_meteograma] Meteograma salvo ' +
                      '(resposta: ' + str(resposta.status_code) + ')')
        else:
            print(' [aranha.obter_meteograma] Erro baixando meteograma: '
                  + str(resposta.status_code))

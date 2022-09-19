"""
Estudo de coleta e visualização de dados de temperatura e probabilidade
de chuva a partir de uma página web.

Obtém dados climáticos do Centro de Previsão de Tempo e Estudos Climáticos
do Instituto de Pesquisas Espaciais (INPE), armazenando os dados em uma
estrutura que permite a consulta para múltiplas cidades.

--------
 Classes
--------
    * Cidade
        * Armazena todas as informações para cada cidade, como o nome, UF,
        dados para plotagem e caminhos de saída dos arquivos.
    * Aranha
        * Recebe uma lista de cidades, verifica se já existem dados baixados
         para cada uma e obtém os dados da rede em caso negativo.
         Requer confirmação antes de cada requisição externa.
    * Tratadora
        * Recebe uma lista de cidades e trata os dados, retirando palavras
        desnecessárias e ordenando os valores para que fiquem apenas os dados
        prontos para plotagem.
    * Plotadora
        * Recebe uma lista de cidades, salva os gráficos em arquivos PNG
        no sistema local e exibe-os usando a interface gráfica do matplotlib.
"""
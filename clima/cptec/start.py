from Cidade import Cidade
from main import main

# define a lista de cidades
sjc = Cidade('São José dos Campos', 'SP')
manaus = Cidade('Manaus', 'AM')
belem = Cidade('Belem', 'PA')
chui = Cidade('Chuí', 'RS')
uiramuta = Cidade('Uiramutã', 'RR')
jp = Cidade('João Pessoa', 'PB')
sjx = Cidade('São José do Xingu', 'MT')
mancio_lima = Cidade('Mâncio Lima', 'AC')
sjdr = Cidade('São João del-Rei', 'MG')
sslr = Cidade('São Sebastião de Lagoa de Roça', 'PB')

cidades = [sjc, manaus, belem, chui, uiramuta, 
           jp, sjx, mancio_lima, sjdr, sslr]

main(cidades)

terminais_default = ['a','b','c','d','e','f','g','h','i','j','&']
nao_terminais_default = ['A','B','C','D','E','F','G','H','I','J','&']
terminais = [] # Lista de Simbolos terminais
nao_terminais = [] # Lista de Simbolos nao terminais

class Simbolo(object):
    #A saida e a entrada será um vetor simbolos
    def __init__(self, valor):
        self.valor = valor
        # tipo 0 terminais tipo 1 nao_terminais
        if valor in terminais: # não alterar a condição
            self.tipo = 0
        else:
            self.tipo = 1

def main():
    print('Construindo a gramática:')
    nr_nao_terminal = int(input('Quantos simbolos não-terminais você deseja?\n'))
    print('Seus simbolos não-terminais são:')
    string = ''
    for x in range(nr_nao_terminal):
        terminais.append(Simbolo(nao_terminais_default[x]))
        if x == nr_nao_terminal -1:
            string += "'" + nao_terminais_default[x] + "'"
        else:
            string += "'" + nao_terminais_default[x] + "', "
    print(string)
    nr_terminal = int(input('Quantos simbolos terminais você deseja?\n'))
    print('Seus simbolos terminais são:')
    string = ''
    for x in range(nr_terminal):
        terminais.append(Simbolo(terminais_default[x]))
        if x == nr_terminal -1:
            string += "'" + terminais_default[x] + "'"
        else:
            string += "'" + terminais_default[x] + "', "
    print(string)

main()
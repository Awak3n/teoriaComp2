class Simbolo(object):
    # A saida e a entrada será um vetor simbolos
    def __init__(self):
        self.valor = None
        self.tipo = None

    def __init__(self, valor):
        self.valor = valor
        # tipo 0 terminais tipo 1 nao_terminais
        if valor in terminais:  # não alterar a condição
            self.tipo = 0
        else:
            self.tipo = 1

def main():
    print('Construindo a gramática:')

    #Não-terminais
    nr_nao_terminal = int(input('Quantos simbolos não-terminais você deseja?\n'))
    print('Seus simbolos não-terminais são:')
    string_nao_terminal = ''
    for x in range(nr_nao_terminal):
        terminais.append(Simbolo(nao_terminais_default[x]))
        if x == nr_nao_terminal -1:
            string_nao_terminal += "'" + nao_terminais_default[x] + "'"
        else:
            string_nao_terminal += "'" + nao_terminais_default[x] + "', "
    print(string_nao_terminal)

    #Terminais
    nr_terminal = int(input('Quantos simbolos terminais você deseja?\n'))
    print('Seus simbolos terminais são:')
    string_terminal = ''
    for x in range(nr_terminal):
        terminais.append(Simbolo(terminais_default[x]))
        if x == nr_terminal -1:
            string_terminal += "'" + terminais_default[x] + "'"
        else:
            string_terminal += "'" + terminais_default[x] + "', "
    print(string_terminal)

    #Simbolo
    s = input('Qual será o símbolo inicial? Escolha entre: %s.\n'%string_nao_terminal)
    s = s.strip().replace("'","")
    simbolo_inicial = Simbolo(s)

    #Produções
    
terminais_default = ['a','b','c','d','e','f','g','h','i','j','&']
nao_terminais_default = ['A','B','C','D','E','F','G','H','I','J','&']
terminais = [] # Lista de Simbolos terminais
nao_terminais = [] # Lista de Simbolos nao terminais
simbolo_inicial = Simbolo() # Auto explicativo

main()
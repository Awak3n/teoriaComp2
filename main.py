class Simbolo(object):
    def __init__(self, valor=None):
        self.valor = valor
        # tipo 0 terminais tipo 1 nao_terminais
        if valor in terminais:  # não alterar a condição
            self.tipo = 0
        elif valor is None:
            self.tipo = None
        else:
            self.tipo = 1

class Producao(object):
    # A saida e a entrada serão um vetor simbolos
    def __init__(self, entrada, saida=[Simbolo('&')]):
        self.entrada = entrada
        self.saida = saida

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
    resposta = input("Além deles, deseja adicionar também a senteça vazia |&|?\n")
    resposta = resposta.strip().lower()
    print('Seus simbolos terminais são:')
    string_terminal = ''
    for x in range(nr_terminal):
        terminais.append(Simbolo(terminais_default[x]))
        if x == nr_terminal -1:
            if resposta == "sim" or resposta == "yes" or resposta == "y" or resposta == "s":
                string_terminal += "'" + terminais_default[x] + "', "
                terminais.append(Simbolo('&'))
                string_terminal += "'&'"
            else:
                string_terminal += "'" + terminais_default[x] + "'"
        else:
            string_terminal += "'" + terminais_default[x] + "', "
    print(string_terminal)

    #Simbolo
    s = input('Qual será o símbolo inicial? Escolha entre: %s.\n'%string_nao_terminal)
    s = s.strip().replace("'","")
    simbolo_inicial = Simbolo(s)

    #Produções
    print("Agora as produções:\n")
    contador = 1
    p_left = ''
    p_right = ''
    while True:
        sintaxe_error = True
        while sintaxe_error:
            p_left = input("Produção %i - Lado esquerdo\n")
            if p_left == "0":
                break
            p_left = p_left.replace(' ','')
            sintaxe_error = False
            #É preciso verificar se há, pelo menos, um não terminal
            um_nao_terminal = False
            for letra in p_left:
                if letra not in nao_terminais_default:
                    if letra not in terminais_default:
                        sintaxe_error = True
                else:
                    um_nao_terminal = True
            if sintaxe_error is True or um_nao_terminal is False:
                print("Erro de Sintaxe\n")
                print("Não esqueça que é preciso que haja pelo menos um não-terminal do lado esquerdo\n"
                      "E que os simbolos precisam estar entre %s e %s" % (string_nao_terminal,string_terminal))
        if p_left == "0":
            break
        sintaxe_error = True
        while sintaxe_error:
            p_right = input("Produção %i - Lado direito\n")
            p_right = p_right.replace(' ','')
            sintaxe_error = False
            for letra in p_right:
                if letra not in nao_terminais_default:
                    if letra not in terminais_default:
                        sintaxe_error = True
            if sintaxe_error is True:
                print("Erro de Sintaxe\n")
                print("Não esqueça que os simbolos precisam estar entre\n%s e %s" % (string_nao_terminal,string_terminal))
        simbolos_entrada = []
        simbolos_saida = []
        for letra in p_left:
            simbolos_entrada.append(Simbolo(letra))
        for letra in p_right:
            simbolos_saida.append(Simbolo(letra))
        producoes.append(Producao(simbolos_entrada,simbolos_saida))
        contador += 1

     # Exibir gramática
terminais_default = ['a','b','c','d','e','f','g','h','i','j','&']
nao_terminais_default = ['A','B','C','D','E','F','G','H','I','J']
terminais = [] # Lista de Simbolos terminais
nao_terminais = [] # Lista de Simbolos nao terminais
simbolo_inicial = Simbolo() # Auto explicativo
producoes = [] # Produções

main()
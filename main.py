def main():
    print('Construindo a gramática:')

    #Não-terminais
    nr_nao_terminal = int(input('Quantos simbolos não-terminais você deseja?\n'))
    print('Seus simbolos não-terminais são:')
    string_nao_terminal = ''
    for x in range(nr_nao_terminal):
        nao_terminais.append(Simbolo(nao_terminais_default[x]))
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
    while(True):
        s = input('Qual será o símbolo inicial? Escolha entre: %s.\n'%string_nao_terminal)
        s = s.strip().replace("'","").upper()
        if s in string_nao_terminal:
            simbolo_inicial = Simbolo(s)
            break
        else:
            print("O simbolo inicial precisa estar entre os não-terminais determinados")

    #Produções
    print("\nAgora as produções:")
    contador = 1
    p_left = ''
    p_right = ''
    while True:
        sintaxe_error = True
        while sintaxe_error:
            if contador > 1:
                p_left = input("Produção %i - Lado esquerdo (0 para parar)\n" % contador)
            else:
                p_left = input("Produção %i - Lado esquerdo\n" % contador)
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
                      "E que os simbolos precisam estar entre %s, %s" % (string_nao_terminal,string_terminal))
        if p_left == "0":
            break
        sintaxe_error = True
        while sintaxe_error:
            p_right = input("Produção %i - Lado direito\n" % contador)
            p_right = p_right.replace(' ','')
            sintaxe_error = False
            for letra in p_right:
                if letra not in nao_terminais_default:
                    if letra not in terminais_default:
                        sintaxe_error = True
            if sintaxe_error is True:
                print("Erro de Sintaxe")
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
    string_producoes = ""
    for producao in producoes:
        for simbolo in producao.entrada:
            string_producoes += simbolo.valor
        string_producoes += "=>"
        for simbolo in producao.saida:
            string_producoes += simbolo.valor
        string_producoes += ", "
    string_producoes = string_producoes[:-2]

    string_nao_terminal = string_nao_terminal.replace("'","")
    string_terminal = string_terminal.replace("'","")
    print("\nGramática resultante:")
    print("({%s},{%s},{%s},%s)" % (string_nao_terminal,string_terminal,string_producoes,simbolo_inicial.valor))

    # Verificar se a gramática é viavel
    # Passo 1: Ver se as produções abrangem t0do o alfebeto
    for simbolo_terminal in terminais:
        abrange_alfabeto = False
        if simbolo_terminal.valor == '&':
            abrange_alfabeto = True
        else:
            for producao in producoes:
                for simbolo_saida in producao.saida:
                    if simbolo_terminal.valor == simbolo_saida.valor:
                        abrange_alfabeto = True
        if abrange_alfabeto is False:
            print("Erro Estrutural")
            print("Cada simbolo terminal precisa aparecer ao menos uma vez, exceto o |&| se houver")
            break
    for simbolo_nao_terminal in nao_terminais:
        abrange_alfabeto = False
        if simbolo_nao_terminal.valor == simbolo_inicial.valor:
            abrange_alfabeto = True
        else:
            for producao in producoes:
                for simbolo_saida in producao.saida:
                    if simbolo_nao_terminal.valor == simbolo_saida.valor: # se achou uma produção do lado direito
                        for producao2 in producoes: # procura o simbolo em outra produção do lado esquerdo
                            for simbolo_entrada in producao2.saida:
                                if simbolo_nao_terminal.valor == simbolo_entrada.valor:
                                    abrange_alfabeto = True
        if abrange_alfabeto is False:
            print("Erro Estrutural")
            print("Cada simbolo nao-terminal precisa aparecer ao menos uma vez em cada lado das produções")
            break

terminais_default = ['a','b','c','d','e','f','g','h','i','j','&']
nao_terminais_default = ['A','B','C','D','E','F','G','H','I','J']
terminais = [] # Lista de Simbolos terminais
nao_terminais = [] # Lista de Simbolos nao terminais
producoes = [] # Produções
global simbolo_inicial # Auto explicativo

class Simbolo(object):
    def __init__(self, valor=None):
        self.valor = valor
        # tipo 0 terminais tipo 1 nao_terminais
        if valor in terminais_default:  # não alterar a condição
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

main()
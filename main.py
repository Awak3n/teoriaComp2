def getNumber(msg):
    try:
        while (True):
            nr_nao_terminal = int(input(msg))
            if nr_nao_terminal >= 1 and nr_nao_terminal <= 26:
                break
    except:
        nr_nao_terminal = getNumber(msg)
    return  nr_nao_terminal

def main():
    ################################
    # 1. Entrada de gramática          
    ################################

    print('Construindo a gramática:')

    #Não-terminais
    nr_nao_terminal = getNumber('Quantos simbolos não-terminais você deseja? (De 1 a 26)\n')
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
    nr_terminal = getNumber('Quantos simbolos terminais você deseja?\n')
    resposta = input("A gramática aceita o símbolo vazio |&|?(S/N)\n")
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
    if len(nao_terminais) == 1:
        print("Seu simbolo inicial será 'A'")
        simbolo_inicial = Simbolo('A')
    else:
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
            um_nao_terminal = False
            for letra in p_left:
                if letra not in nao_terminais_default[:nr_nao_terminal]:
                    if letra not in terminais_default[:nr_terminal] and letra != '&':
                        sintaxe_error = True
                else: #É preciso verificar se há, pelo menos, um não terminal
                    um_nao_terminal = True
            if sintaxe_error is True or um_nao_terminal is False:
                sintaxe_error = True
                print("Erro de Sintaxe\n")
                print("Não esqueça que é preciso que haja pelo menos um não-terminal do lado esquerdo\n"
                      "E que os simbolos precisam estar entre %s, %s\n" % (string_nao_terminal,string_terminal))
        if p_left == "0":
            break
        sintaxe_error = True
        while sintaxe_error:
            p_right = input("Produção %i - Lado direito\n" % contador)
            p_right = p_right.replace(' ','')
            sintaxe_error = False
            if p_right[0] == '|':
                p_right = p_right[1:]
            if p_right[-1] == '|':
                p_right = p_right[:-1]
            for letra in p_right:
                if letra != '|':
                    if letra not in nao_terminais_default[:nr_nao_terminal]:
                        if letra not in string_terminal.replace("'",""):
                            sintaxe_error = True
            if sintaxe_error is True:
                print("Erro de Sintaxe")
                print("Não esqueça que os simbolos precisam estar entre\n%s e %s" % (string_nao_terminal,string_terminal))
        simbolos_entrada = []
        simbolos_saida = []
        for letra in p_left:
            simbolos_entrada.append(Simbolo(letra))
        p_right += '|'
        for letra in p_right:
            if letra == '|':
                if len(simbolos_saida) > 1:
                    for simbolo in simbolos_saida:
                        if simbolo.valor == '&':
                            print("Aviso:")
                            print("A sentença vazia somente pode ser encontrada sozinha no lado direito, demais simbolos foram ignorados\n")
                            simbolos_saida = [Simbolo('&')]
                producoes.append(Producao(simbolos_entrada, simbolos_saida))
                simbolos_saida = []
            else:
                simbolos_saida.append(Simbolo(letra))
        p_right = p_right[:-1]
        contador += 1

    ################################
    # 2. Exibir gramática          
    ################################
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
    print("({%s},{%s},{%s},%s)\n" % (string_nao_terminal,string_terminal,string_producoes,simbolo_inicial.valor))

    ################################
    # 3. Verificação da gramática          
    ################################
    # Passo 1: Ver se as produções abrangem todo o alfabeto
    # Passo 2: Evitar loopings obvios (quando não há nem sequer uma produção com apenas terminais)
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
        contador_p1 = 0
        contador_p2 = 0
        is_a_looping = True
        if simbolo_nao_terminal.valor == simbolo_inicial.valor: # se ele é o simbolo inicial, ele automaticamente abrange o alfabeto
            abrange_alfabeto = True
        for producao in producoes:
            only_terminais = True
            for simbolo_saida in producao.saida:
                if only_terminais is False or simbolo_saida.tipo == 1: # verifica se há apenas terminais no lado direito dessa produção
                    only_terminais = False
                if simbolo_nao_terminal.valor == simbolo_saida.valor: # se achou uma produção do lado direito
                    for producao2 in producoes: # procura o simbolo em outra produção do lado esquerdo em outra produção
                        for simbolo_entrada in producao2.saida:
                            if contador_p1 != contador_p2 and simbolo_nao_terminal.valor == simbolo_entrada.valor:
                                abrange_alfabeto = True
                            contador_p2 += 1
            if only_terminais is True:
                is_a_looping = False
            contador_p1 += 1
        if abrange_alfabeto is False:
            print("Erro Estrutural")
            print("Cada simbolo nao-terminal precisa aparecer ao menos uma vez em cada lado das produções e em produções diferentes, exceto o simbolo inicial")
        break
    ################################
    # 4. Identificação da Gramática
    ################################

    for terminal in terminais:
        print(terminal.valor)
        print(terminal.tipo)

    ################################
    # 5. Geração de Sentenças
    ################################


    ################################
    # 6. Autômato Finito          
    ################################

terminais_default = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','&']
nao_terminais_default = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
terminais = [] # Lista de Simbolos terminais
nao_terminais = [] # Lista de Simbolos nao terminais
producoes = [] # Produções
global simbolo_inicial # Símbolo Inicial da Gramática

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

    def getValorEsquerdo(self):
        string = ""
        for simbolo in self.entrada:
            string += simbolo.valor
        return string

    def getValorDireito(self):
        string = ""
        for simbolo in self.saida:
            string += simbolo.valor
        return string
main()
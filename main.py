import random as rng
import copy
import texttable

#Pega o número de NT desejados e o converte em 'n' NT
def getNumber(msg):
    try:
        while (True):
            nr_nao_terminal = int(input(msg))
            if nr_nao_terminal >= 1 and nr_nao_terminal <= 10:
                break
    except:
        nr_nao_terminal = getNumber(msg)
    return  nr_nao_terminal

def checkGramatica():
    #retorna o tipo de gramática (0 para GI,1 para GSC,2 para GLC,3 para GR)
    #irá verificar se as produções seguem as regras dos tipos de gramática da hierarquia de Chomsky
    type3 = True
    type2 = True
    type1 = True
    for producao in producoes:
        #caso possua mais de um símbolo de entrada ou o mesmo seja um T, não pode ser GLC ou GR
        if (len(producao.entrada) > 1 or producao.entrada[0].tipo == 0):
            type3 = False
            type2 = False
        #caso o tamanho do lado esquerdo seja maior que o lado direito, não pode ser GSC
        if (len(producao.entrada) > len(producao.saida)):
            type1 = False
        #caso não possua somente um NT ou um NT e um T de produção, não pode ser GR
        if ((len(producao.saida) == 1 and producao.saida[0].tipo == 1) or len(producao.saida) >= 2):
            if (producao.saida[0].tipo != 0 or producao.saida[1].tipo != 1):
                type3 = False
        #caso possua símbolo vazio, não pode ser GSC ou GLC
        for simbolo in producao.saida:
            if simbolo.valor == '&':
                type2 = False
                type1 = False
    if type3:
        return [3,"Regular"]
    elif type2:
        return [2,"Livre de Contexto"]
    elif type1:
        return [1,"Sensível ao Contexto"]
    else:
        return [0,"Irrestrita"]

def main():
    global nao_terminais, simbolo_inicial, terminais, producoes
    ################################
    # 1. Entrada de gramática          
    ################################

    print('Construindo a gramática:')

    #Não-terminais
    #Gera os não-terminais automáticamente
    nr_nao_terminal = getNumber('Quantos simbolos não-terminais você deseja? (De 1 a 10)\n')
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
    # Gera os terminais automáticamente
    nr_terminal = getNumber('Quantos simbolos terminais você deseja?\n')
    print('Seus simbolos terminais são:')
    string_terminal = ''
    for x in range(nr_terminal):
        terminais.append(Simbolo(terminais_default[x]))
        string_terminal += "'" + terminais_default[x] + "', "
    print(string_terminal)
    terminais.append(Simbolo('&'))
    for terminal in terminais:
        terminais_string_list.append(terminal.valor)
    for nao_terminal in nao_terminais:
        nao_terminais_string_list.append(nao_terminal.valor)

    #Simbolo
    #Pergunta e valida o simbolo inicial
    if len(nao_terminais) == 1:
        print("Seu simbolo inicial será 'A'\n")
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
    #Input e validação inicial das produções
    print("\nAgora as produções: (MÁXIMO 10)")
    contador = 1
    p_left = ''
    p_right = ''
    while len(producoes) < 11:
        sintaxe_error = True
        #Criando a produção do lado esquerdo
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
                #verifica se os simbolos escolhidos abrangem o alfabeto
                if letra not in nao_terminais_default[:nr_nao_terminal]:
                    if letra not in terminais_default[:nr_terminal] and letra != '&': 
                        sintaxe_error = True
                #É preciso verificar se há, pelo menos, um não terminal no lado esquerdo
                else: 
                    um_nao_terminal = True
            if sintaxe_error is True or um_nao_terminal is False:
                sintaxe_error = True
                print("Erro de Sintaxe\n")
                print("Não esqueça que é preciso que haja pelo menos um não-terminal do lado esquerdo\n"
                      "E que os simbolos precisam estar entre %s, %s\n" % (string_nao_terminal,string_terminal))
        if p_left == "0":
            break
        sintaxe_error = True
        # Criando a produção do lado direito
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
                        if letra != '&':
                            #verifica se o lado direito abrange o alfabeto
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
        #Verifica se o símbolo vazio está presente no lado direito
        for letra in p_right:
            if letra == '|':
                if len(simbolos_saida) > 1:
                    for simbolo in simbolos_saida:
                        #caso esteja, remove todos os outros T e NT que a acompanham
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

    transformacaoGLC()
    getAllFirst()
    getAllFollow()
    print("\nFirsts:")
    print(firsts)
    print("\nFollows:")
    print(follows)
    print("\nTabela:") # montar isso bonitinho amanhã se sobrar tempo
    tabelaPretty = texttable.Texttable()
    for (keyPilha,keyEntrada) in tabela:
        tabelaPretty.add_rows([["NT na Pilha", "T na Entrada", "Saída"],[keyPilha,keyEntrada,tabela[(keyPilha,keyEntrada)]]])
    print(tabelaPretty.draw() + '\n')
    reconhecimentoDeEntrada()

def transformacaoGLC():
    '''Método contendo todas as transformações, para debbuging'''
    fatoracao()
    recursaoAEsquerda()

def eLivre():
    '''Remove o símbolo vazio &'''
    global producoes, terminais, nao_terminais, simbolo_inicial
    # exemplo 2
    # terminais = [Simbolo('a'), Simbolo('b')]  # Lista de Simbolos terminais
    # nao_terminais = [Simbolo('A'), Simbolo('B')]  # Lista de Simbolos nao terminais
    # producoes = [Producao([Simbolo('A')], [Simbolo('a'), Simbolo('B')]),
    #              Producao([Simbolo('A')], [Simbolo('a'), Simbolo('a'), Simbolo('B')]),
    #              Producao([Simbolo('A')], [Simbolo('b'), Simbolo('A')]),
    #              Producao([Simbolo('A')], [Simbolo('a'), Simbolo('B'), Simbolo('b')]),
    #              Producao([Simbolo('B')], [Simbolo('b'), Simbolo('B')]),
    #              Producao([Simbolo('B')], [Simbolo('&')])]  # Produções
    # simbolo_inicial = Simbolo('A')  # Símbolo Inicial da Gramática

    print("\nEntrando na Remoção de & (&-livre)\n")

    print("\nProduções Iniciais: ", producoes, '\n')
    producoes_aux = []
    tamanho = len(producoes)
    for producao in producoes:
        if producao.getValorDireito() == '&':
            for p in range(tamanho):
                if producao.getValorEsquerdo() in producoes[p].getValorDireito():
                    producao_auxiliar = copy.deepcopy(producoes[p])
                    producoes_aux.append(producao_auxiliar)
                    for simbolo_entrada in producao.entrada:
                        for simbolo_saida in producoes[p].saida:
                            if simbolo_entrada.valor == simbolo_saida.valor:
                                producoes[p].saida.remove(simbolo_saida)
            producoes.remove(producao)
    producoes.extend(producoes_aux)
    print("\nProduções Resultantes: ", producoes, '\n')

def remocaoUnitaria():
    '''Remove produções unitárias'''
    global producoes, terminais, nao_terminais, simbolo_inicial
    # exemplo 3
    # terminais = [Simbolo('a'), Simbolo('b')]  # Lista de Simbolos terminais
    # nao_terminais = [Simbolo('A'), Simbolo('B')]  # Lista de Simbolos nao terminais
    # producoes = [Producao([Simbolo('B')], [Simbolo('b'), Simbolo('B')]), Producao([Simbolo('B')], [Simbolo('A')]),
    #              Producao([Simbolo('A')], [Simbolo('a'), Simbolo('A')]),
    #              Producao([Simbolo('A')], [Simbolo('a')])]  # Produções
    # simbolo_inicial = Simbolo('B')  # Símbolo Inicial da Gramática
    print("\nEntrando na Remoção de Produções Unitárias\n")

    print("\nProduções Iniciais: ", producoes, '\n')
    valores_nao_terminais = []
    for simbolo in nao_terminais:
        valores_nao_terminais.append(simbolo.valor)
    producoes_semelhantes = []
    producoes_concluidas = []
    for producao in producoes:
        if producao.getValorEsquerdo() in valores_nao_terminais and producao.getValorEsquerdo() not in producoes_concluidas:
            for prod in producoes:
                if prod.getValorEsquerdo() == producao.getValorEsquerdo():
                    producoes_semelhantes.append(prod)
            for prod in producoes:
                if producao.getValorEsquerdo() == prod.getValorDireito():
                    for ps in producoes_semelhantes:
                        producoes.append(Producao(prod.entrada, ps.saida))
                    producoes.remove(prod)
            producoes_concluidas.append(producao.getValorEsquerdo())
        producoes_semelhantes = []
    print("\nProduções Resultantes: ", producoes, '\n')

def fatoracao():
    '''Realiza a fatoração'''
    global producoes, nao_terminais, simbolo_inicial
    # exemplo 4.1
    # terminais = [Simbolo('a'), Simbolo('b')]  # Lista de Simbolos terminais
    # nao_terminais = [Simbolo('A'), Simbolo('B'), Simbolo('C')]  # Lista de Simbolos nao terminais
    # producoes = [Producao([Simbolo('A')], [Simbolo('a'), Simbolo('A')]), Producao([Simbolo('A')], [Simbolo('a')]),
    #              Producao([Simbolo('B')], [Simbolo('b')]), Producao([Simbolo('C')], [Simbolo('a'), Simbolo('A')]),
    #              Producao([Simbolo('C')], [Simbolo('a'), Simbolo('B')])]  # Produções
    # simbolo_inicial = Simbolo('C')  # Símbolo Inicial da Gramática

    # exemplo 4.2
    # terminais = [Simbolo('a'),Simbolo('b')] # Lista de Simbolos terminais
    # nao_terminais = [Simbolo('A'),Simbolo('B'),Simbolo('C')] # Lista de Simbolos nao terminais
    # producoes = [Producao([Simbolo('A')],[Simbolo('B'),Simbolo('b')]),Producao([Simbolo('A')],[Simbolo('a'),Simbolo('B')]),Producao([Simbolo('B')],[Simbolo('a')]),Producao([Simbolo('C')],[Simbolo('b')]), Producao([Simbolo('C')],[Simbolo('a'),Simbolo('B')])] # Produções
    # simbolo_inicial = Simbolo('A') # Símbolo Inicial da Gramática
    print("\nEntrando na Fatoração\n")

    print("\nProduções Iniciais: ", producoes, '\n')
    # não testado
    # primeiro precisamos substituir todas expressoes que começam com um simbolo nao-terminal
    # for producao in producoes:
    #     if producao.getValorDireito()[0] in nao_terminais_default:
    #         producoes_semelhantes = []
    #         for prod in producoes:
    #             if prod.getValorEsquerdo() == producao.getValorEsquerdo():
    #                 producoes_semelhantes.append(prod)
    #         for ps in producoes_semelhantes:
    #             saida = copy.deepcopy(producao.saida)
    #             del(saida[0])
    #             ps_saida = copy.deepcopy(ps.saida)
    #             ps_saida.extend(saida)
    #             producoes.append(Producao(producao.entrada, ps_saida))
    #         producoes.remove(producao)
    # depois de pronto podemos finalmente fatorar

    print("\nProduções pronta para a fatoração: ", producoes, '\n')

    # procurando produções que possuam ambiguidade
    terminais_found = {}  # terminais encontrados para cada símbolo
    for simbolo in nao_terminais:
        terminais_found[simbolo] = {}
        for t in terminais:
            terminais_found[simbolo][t.valor] = 0
        for producao in producoes:
            if producao.entrada[0].valor == simbolo.valor:
                # começa a verificar
                if producao.saida[0].tipo == 0:
                    terminais_found[simbolo][producao.saida[0].valor] += 1
                    # removendo ambiguidade e adicionando novos não terminais
    for simbolo in terminais_found:
        for terminal in terminais_found[simbolo]:
            current = terminais_found[simbolo][terminal]
            # se ambiguidade for encontrada
            if current >= 2:
                print("Ambiguidade encontrada: Símbolo %s -> Terminal %s" % (simbolo, terminal))
                producoes.append(
                    Producao([insereNovoNaoTerminal(simbolo, terminal)],
                             [Simbolo(terminal), simbolo]))
    print("\nProduções Resultantes: ", producoes, '\n')

def insereNovoNaoTerminal(simbolo, terminal):
    '''Insere um novo NT, recebendo de parâmetro as produções, a lista de NT, o símbolo vítima e o terminal a ser destruído'''
    novo_simbolo = Simbolo(nao_terminais_default[len(nao_terminais)])
    nao_terminais.append(novo_simbolo)
    for producao in producoes:
        if producao.entrada[0].valor == simbolo.valor:
            if producao.entrada[0].valor == simbolo_inicial.valor:
                simbolo_inicial.valor = novo_simbolo.valor
            for elem in producao.saida:
                if elem.valor == terminal:
                    producao.saida.remove(elem)
            if len(producao.saida) == 0:
                producao.saida.append(Simbolo('&'))
    return novo_simbolo

def recursaoAEsquerda():
    '''Remove recursão geral à esquerda'''
    global producoes, nao_terminais, terminais

    print("\nEntrando na Remoção de Recursão à Esquerda\n")
    print("\nProduções Iniciais: ", producoes, '\n')
    #s_nt - itera os simbolos NT
    #p_nt - itera as producoes NT
    for s_nt in range(len(nao_terminais)):
        for p_nt in range(int(s_nt+1)):
            recursoesImediatas = []
            p = 0
            while p < len(producoes):
                if producoes[p].entrada[0].valor == nao_terminais[s_nt].valor and producoes[p].saida[0].valor == nao_terminais[p_nt].valor:
                    if producoes[p].saida[0].valor == nao_terminais[s_nt].valor:
                        recursoesImediatas.append(producoes[p])
                        del(producoes[p])
                        p -= 1
                    else:
                        producaoExcluida = copy.deepcopy(producoes[p])
                        producaoExcluida.saida = producaoExcluida.saida[1:]
                        for producao in producoes:
                            if producao.entrada[0].valor == nao_terminais[p_nt].valor:
                                aux = copy.deepcopy(producao.saida)
                                aux.extend(producaoExcluida.saida)
                                producoes.append(Producao([Simbolo(nao_terminais[s_nt].valor)],aux))
                        del(producoes[p])
                        p -= 1
                p += 1
            #remove recursoes imediatas
            if recursoesImediatas:
                novo_simbolo = Simbolo(nao_terminais_default[len(nao_terminais)])
                nao_terminais.append(novo_simbolo)
                if '&' not in terminais_string_list:
                    terminais.append(Simbolo('&'))
                    terminais_string_list.append('&')
                for producao in producoes:
                    if producao.entrada[0].valor == nao_terminais[s_nt].valor:
                        producao.saida.append(novo_simbolo)
                for producao in recursoesImediatas:
                    producao.entrada = [novo_simbolo]
                    nova_saida = producao.saida[1:]
                    nova_saida.append(novo_simbolo)
                    producao.saida = nova_saida
                    producoes.append(producao)
                producoes.append(Producao([novo_simbolo],[Simbolo('&')]))

    print("\nProduções Resultantes: ", producoes, '\n')

def getAllFirst():
    '''Faz as chamadas de funções para calcular os firsts de todos os nao terminais'''
    for nao_terminal in nao_terminais:
        getFirstByNaoTerminal(nao_terminal)

def firstRecursivo(posicao_da_producao, producao, resultado):
    """Caso o Nao Terminal tenha um nao terminal como first calcula o first do nao terminal"""
    global firsts
    temVazio = None
    for first in firsts:
        try:
            if producao.saida[posicao_da_producao] == first.nao_terminal:
                temVazio = False
                for producao_first in first.valor:
                    if producao_first.valor == '&':
                        temVazio = True
                if not temVazio:
                    string_resultado_list = []
                    for r in resultado:
                        string_resultado_list.append(r.valor)
                    for f in first:
                        if f.valor not in string_resultado_list:
                            resultado.append(f)
                    tabela[producao.entrada[0].valor, producao_first.valor] = producao
                else:
                    firstRecursivo(posicao_da_producao + 1, producao, first)
        except:
            pass
    if temVazio is None:
        first = getFirstByNaoTerminal(producao.saida[posicao_da_producao])
        string_resultado_list = []
        for r in resultado:
            string_resultado_list.append(r.valor)
        for f in first:
            if f.valor not in string_resultado_list:
                resultado.append(f)
    return resultado

def getFirstByNaoTerminal(nao_terminal):
    """Obtem o first com base no nao terminal passado como parametro"""
    global firsts, tabela
    first = []
    for producao in producoes:
        if producao.entrada[0].valor == nao_terminal.valor:
            if producao.saida[0].valor in terminais_string_list:
                first.append(producao.saida[0])
                tabela[producao.entrada[0].valor,producao.saida[0].valor] = producao
            elif producao.saida[0].valor in nao_terminais_string_list:
                first = firstRecursivo(0, producao, first)
                for f in first:
                    tabela[producao.entrada[0].valor,f.valor] = producao
    jaFoiAdiconado = False
    for f in firsts:
        if nao_terminal.valor == f.nao_terminal.valor:
            jaFoiAdiconado = True
    if not jaFoiAdiconado:
        firsts.append(FirstOrFollow(nao_terminal, first))
    return first

def getAllFollow():
    """Faz as chamadas de funções para calcular os follows de todos os nao terminais"""
    global follows
    cont = 0
    for nao_terminal in nao_terminais:
        follow = []
        if cont == 0:
            follow.append(Simbolo('$'))
        for producao in producoes:
            if nao_terminal.valor in producao.getValorDireito():
                for simbolo in range(len(producao.saida)):
                    if producao.saida[simbolo].valor == nao_terminal.valor:
                        if simbolo + 1 == len(producao.saida):
                            for f in follows:
                                if producao.entrada[0].valor == f.nao_terminal.valor:
                                    follow.extend(f.valor)
                        else:
                            if producao.saida[simbolo + 1].valor in terminais_string_list and producao.saida[simbolo + 1].valor != '&':
                                follow.append(producao.saida[simbolo + 1])
                            elif producao.saida[simbolo + 1].valor in nao_terminais_string_list:
                                for f in firsts:
                                    if producao.saida[simbolo + 1].valor == f.nao_terminal.valor:
                                        follow.extend(f.valor)
                                if derivaVazio(producao.saida[simbolo + 1]):
                                    for f in follows:
                                        if producao.entrada[0].valor == f.nao_terminal.valor:
                                            follow.extend(f.valor)
        # limpa vazios e valores repetidos
        follow_list = []
        f = 0
        while f < len(follow):
            if follow[f].valor == '&' or follow[f].valor in follow_list:
                follow.remove(follow[f])
            else:
                follow_list.append(follow[f].valor)
                f += 1
        follows.append(FirstOrFollow(nao_terminal, follow))
        if derivaVazio(nao_terminal):
            for simbolo in follow:
                tabela[nao_terminal.valor,simbolo.valor] = Producao([Simbolo(nao_terminal.valor)], [Simbolo('&')])
        cont += 1

def derivaVazio(simbolo):
    deriva = False
    for producao in producoes:
        if producao.entrada[0].valor == simbolo.valor:
            if producao.saida[0].valor == '&':
                deriva = True
    return deriva

def listaToStr(lista):
    listaStr = ''
    for l in lista:
        listaStr += l
    return listaStr

terminais_default = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','&','(',')','[',']','+','*']
nao_terminais_default = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
terminais = [] # Lista de Simbolos terminais
nao_terminais = [] # Lista de Simbolos nao terminais
nao_terminais_string_list = []
terminais_string_list = []
producoes = [] # Produções
simbolo_inicial = None # Símbolo Inicial da Gramática
firsts = [] # Firsts
follows = [] # Follows
tabela = {} # Tabela de Análise

class Simbolo(object):
    def __init__(self, valor=None):
        self.valor = valor
        # tipo 0 terminais tipo 1 nao_terminais
        if valor in terminais_default:  # não alterar a condição
            self.tipo = 0
        elif valor is None or valor == '$':
            self.tipo = None
        else:
            self.tipo = 1
    def __repr__(self):
        return self.valor

class FirstOrFollow(object):
    def __init__(self, nao_terminal, valor):
        self.nao_terminal = nao_terminal
        self.valor = valor #valor é um vetor de simbolos terminais
    def __repr__(self):
        return str(self.nao_terminal) + " -> " + str(self.valor)

class Producao(object):
    # A saida e a entrada serão um vetor simbolos
    def __init__(self, entrada, saida=[Simbolo('&')]):
        self.entrada = entrada
        self.saida = saida

    def getValorEsquerdo(self):
        """Retorna o valor esquerdo da produção"""
        string = ""
        for simbolo in self.entrada:
            string += simbolo.valor
        return string

    def getValorDireito(self):
        """Retorna o valor direito da produção"""
        string = ""
        for simbolo in self.saida:
            string += simbolo.valor
        return string
    
    def __repr__(self):
         return str(self.entrada)+' -> '+str(self.saida)

def mainExemplo():
    global terminais, nao_terminais, producoes, simbolo_inicial
    # Gramática 1
    # A => CB
    # B => bCB | &
    # C => a
    # codificado:
    terminais = [Simbolo('a'), Simbolo('b'), Simbolo('&')]  # Lista de Simbolos terminais
    nao_terminais = [Simbolo('A'), Simbolo('B'), Simbolo('C')]  # Lista de Simbolos nao terminais
    producoes = [Producao([Simbolo('A')], [Simbolo('C'), Simbolo('B')]), Producao([Simbolo('B')], [Simbolo('b'), Simbolo('C'), Simbolo('B')]),
                Producao([Simbolo('B')], [Simbolo('&')]), Producao([Simbolo('C')], [Simbolo('a')])]  # Produções
    simbolo_inicial = Simbolo('A')  # Símbolo Inicial da Gramática
    # Gramática 2
    # E = TG
    # G = +TG | &
    # T = FU
    # U = *FU | &
    # F = (E) | x
    # codificado
    # terminais = [Simbolo('x'), Simbolo('+'), Simbolo('*'), Simbolo('('), Simbolo(')'), Simbolo('&')]  # Lista de Simbolos terminais
    # nao_terminais = [Simbolo('E'), Simbolo('G'), Simbolo('T'), Simbolo('U'), Simbolo('F'),]  # Lista de Simbolos nao terminais
    # producoes = [Producao([Simbolo('E')], [Simbolo('T'), Simbolo('G')]), Producao([Simbolo('G')], [Simbolo('+'), Simbolo('T'), Simbolo('G')]), Producao([Simbolo('G')], [Simbolo('&')]),
    #            Producao([Simbolo('T')], [Simbolo('F'), Simbolo('U')]), Producao([Simbolo('U')], [Simbolo('*'), Simbolo('F'), Simbolo('U')]), Producao([Simbolo('U')], [Simbolo('&')]),
    #            Producao([Simbolo('F')], [Simbolo('('), Simbolo('E'), Simbolo(')')]), Producao([Simbolo('F')], [Simbolo('x')])]  # Produções
    # simbolo_inicial = Simbolo('E')  # Símbolo Inicial da Gramática
    # Gramática 3
    # A = Ca | Bd
    # B = Aa | Ce
    # C = A | B | f
    # codificado
    # terminais = [Simbolo('a'), Simbolo('d'), Simbolo('e'), Simbolo('f')]  # Lista de Simbolos terminais
    # nao_terminais = [Simbolo('A'), Simbolo('B'), Simbolo('C')]  # Lista de Simbolos nao terminais
    # producoes = [Producao([Simbolo('A')], [Simbolo('C'), Simbolo('a')]), Producao([Simbolo('A')], [Simbolo('B'), Simbolo('d')]),
    #           Producao([Simbolo('B')], [Simbolo('A'),Simbolo('a')]), Producao([Simbolo('B')], [Simbolo('C'), Simbolo('e')]),
    #           Producao([Simbolo('C')], [Simbolo('A')]), Producao([Simbolo('C')], [Simbolo('B')]),
    #           Producao([Simbolo('C')], [Simbolo('f')])]
    # simbolo_inicial = Simbolo('A')  # Símbolo Inicial da Gramática

    for terminal in terminais:
        terminais_string_list.append(terminal.valor)
    for nao_terminal in nao_terminais:
        nao_terminais_string_list.append(nao_terminal.valor)
    
    transformacaoGLC()
    getAllFirst()
    getAllFollow()
    print("\nFirsts:")
    print(firsts)
    print("\nFollows:")
    print(follows)
    print("\nTabela:") # montar isso bonitinho amanhã se sobrar tempo
    tabelaPretty = texttable.Texttable()
    for (keyPilha,keyEntrada) in tabela:
        tabelaPretty.add_rows([["NT na Pilha", "T na Entrada", "Saída"],[keyPilha,keyEntrada,tabela[(keyPilha,keyEntrada)]]])
    print(tabelaPretty.draw() + '\n')
    reconhecimentoDeEntrada()

def reconhecimentoDeEntrada():
    '''Realiza o reconhecimento de uma entrada'''
    # Para utilizar os exemplos, basta comentar este código inicial 
    # e descomentar o código do exemplo desejado para gramática escolhida
    entrada_manual = input("Insira a entrada a ser reconhecida (sem espaços): ")
    entrada_manual = entrada_manual.replace(' ','')
    entrada = []
    for char in entrada_manual:
        entrada.append(char)

    # Pacote de exemplos para a Gramática 1
    # Exemplo 1 (não reconhece)
    # entrada = ["a","b","b","b","a"]
    # Exemplo 2 (reconhece)
    # entrada = ["a","b","a","b","a","b","a","b","a","b","a"]
    #
    # Pacote de exemplos para a Gramática 2
    # Exemplo 1 (não reconhece)
    # entrada = ["x","+","+","x"]
    # Exemplo 2 (reconhece)
    # entrada = ["(","x",")","+","(","x","*","(","x","+","x",")",")","*","x"]
    #
    # Pacote de exemplos para a Gramática 3
    # Exemplo 1 (não reconhece)
    # entrada = ["f"]
    # Exemplo 2 (reconhece)
    # entrada = ["f","a","a","d"]

    entrada.append("$") 
    entrada.reverse() #revertendo para poder tratar como uma pilha
    pilha = ["$",simbolo_inicial.valor]
    saida = ""
    table = texttable.Texttable()
    table.add_rows([["Pilha", "Entrada", "Saída"],[listaToStr(pilha),listaToStr(entrada)[::-1],saida]])
    
    #loop principal de reconhecimento
    while pilha[len(pilha)-1] != "$" or entrada[len(entrada)-1] != "$":
        #Regras:
        # Se tem NT na pilha, verifica na tabela se reconhece 
        # e substituiu na pilha o NT pelo lado direito (pop NT e push lado direito)
        topoP = len(pilha)-1
        topoE = len(entrada)-1
        if (pilha[topoP] in nao_terminais_default):
            if (pilha[topoP],entrada[topoE]) in tabela:
                saida = tabela[(pilha[topoP],entrada[topoE])] #producao
                direito = copy.deepcopy(saida.saida)
                pilha.pop()
                if(direito[0].valor != "&"):
                    direito.reverse()
                    for elem in direito:
                        pilha.append(elem.valor)
            else:
                print(table.draw())
                print("Erro: Entrada não reconhecida.")
                return
        elif (pilha[topoP] in terminais_default):
            # Se tem T na pilha e o mesmo T na entrada, elimina ambos (reconhece)
            if (pilha[topoP] == entrada[topoE]):
                saida = ''
                pilha.pop()
                entrada.pop()
            else:
                print(table.draw())
                print("Erro: Entrada não reconhecida.")
                return
        else:
            print(table.draw())
            print("Erro: Entrada não reconhecida.")
            return
        table.add_rows([["Pilha", "Entrada", "Saída"],[listaToStr(pilha),listaToStr(entrada)[::-1],saida]])
    print('\n' + table.draw() + '\n')
    print("Entrada reconhecida com sucesso!")


main()
#mainExemplo()
